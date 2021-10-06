from typing import Dict, List

from django.conf import settings
from django.db import models
from django.db.models.functions import Cast
from django.utils import timezone

from main.apps.companies.models import Company
from main.apps.credit.models import CreditBalance
from main.apps.credit import constants as credit_const
from main.apps.companies import utils as company_utils
from main.apps.fakturoid_app import utils as fakturoid_utils

from .models import Invoice
from ..fakturoid_app.exceptions import FakturoidException


def generate_invoices():
    """ Vystavuje faktury za pro všechny Companies. """

    for company in Company.objects.all():
        generate_invoice_for_company(company)


def generate_invoice_for_company(company: Company):
    """ Vystavuje faktury za Payments pouze typu Provize, Poplatky"""
    # todo need test

    subject_id = get_or_create_fakturoid_subject(company)

    # vytvořím řádky na faktuře
    credit_qs = CreditBalance.objects.filter(study__company=company).for_invoice().not_invoiced()

    if len(credit_qs) == 0:
        return

    raw_data = generate_invoice_data(credit_qs)
    fakturoid_data = transform_payment_data_to_fakturoid(raw_data)
    fa_lines = fakturoid_utils.create_fakturoid_invoice_lines(fakturoid_data)

    # vytvořím fakturu
    try:
        fa_invoice = fakturoid_utils.create_invoice(subject_id, fa_lines, proforma=False)
    except FakturoidException:
        fa_invoice = None

    credit_qs.update(invoiced_on=timezone.now())

    invoice = Invoice(
        company=company,
        fakturoid_invoice_id=fa_invoice.id if fa_invoice else None,
        invoice_number=fa_invoice.number if fa_invoice else None,
        fakturoid_public_url=fa_invoice.public_html_url if fa_invoice else None,
        issue_date=timezone.now().date(),
        amount=fa_invoice.total if fa_invoice else sum([item['total'] for item in raw_data])
    )
    invoice.save()


def generate_invoice_data(credit_qs) -> List[Dict]:

    data = credit_qs \
        .values('study', 'balance_type', 'vat_rate') \
        .annotate(total=Cast(models.Sum('balance_amount') / (settings.INT_RATIO * -1), output_field=models.FloatField())) \
        .values('total', 'balance_type', 'study__number', 'vat_rate') \
        .order_by('total')
    return list(data)


def transform_payment_data_to_fakturoid(data: List[Dict]) -> List[Dict]:
    """

    @:return ... data for Fakturoid invoice line in this format
    {
       'quantity': 1,
       'name': 'Provize',
       'unit_name': 'ks',
       'unit_price_with_vat': 100,  # cena bez DPH
       'vat_rate': 21,
     }
    """
    name_mapper = {
        credit_const.CREDIT_BALANCE_BANK_TRANSFER_FEE: 'Poplatky za bankovní převod',
        credit_const.CREDIT_BALANCE_COMMISSION: 'Provize',
        credit_const.CREDIT_BALANCE_POST_OFFICE_FEE: 'Poplatky za poštovní poukázky',
    }

    transformed_data = []
    for item in data:
        transformed_data.append({
            'quantity': 1,
            'name': '{} {}'.format(name_mapper[item['balance_type']], item['study__number']),
            'unit_name': 'ks',
            'unit_price_with_vat': item['total'],
            'vat_rate': item['vat_rate'],
        })
    return transformed_data


def get_or_create_fakturoid_subject(company: Company):
    # todo need test

    # vytvořím subject pokud ještě nemám
    if company.fa_subject_id is None:
        subject_data = company_utils.get_company_data_for_fakturoid(company)
        fa = fakturoid_utils.get_fakturoid_account()
        subject = fakturoid_utils.create_fakturoid_subject(fa, subject_data)
        company.fa_subject_id = subject.id
        company.save()
    return company.fa_subject_id
