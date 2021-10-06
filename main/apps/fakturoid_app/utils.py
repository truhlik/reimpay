import datetime
import logging
import time
from typing import Dict, List, Any

import requests
from constance import config

from django.conf import settings
from django.utils import timezone

from fakturoid import Fakturoid, Subject, Invoice, InvoiceLine

from main.apps.fakturoid_app.exceptions import FakturoidException

logger = logging.getLogger(__name__)


def get_fakturoid_invoice_pdf_url(invoice_id):
    return 'https://app.fakturoid.cz/api/v2/accounts/{}/invoices/{}/download.pdf'\
        .format(config.FAKTUROID_SLUG, invoice_id)


def get_fakturoid_account():
    if not all([config.FAKTUROID_SLUG, config.FAKTUROID_EMAIL, config.FAKTUROID_API_KEY]):
        raise FakturoidException('Fakturoid account is not set')
    fa = Fakturoid(config.FAKTUROID_SLUG, config.FAKTUROID_EMAIL, config.FAKTUROID_API_KEY, 'Reimpay')
    return fa


def create_fakturoid_subject(fa: Fakturoid, data: Dict[str, str]) -> Subject:
    """
    Vytvoř kontakt na Fakturoidu.
    :param fa: Fakturoid
    :param data:
    :return: Subject
    """

    subject = Subject(
        name=data['name'],
        street=data['street'],
        city=data['city'],
        zip=data['zip'],
        registration_no=data['registration_no'],
        vat_no=data['vat_no'],
        email=data['email'],
        phone=data['phone'],
    )
    if fa is not None:
        fa.save(subject)
    return subject


def create_fakturoid_invoice_lines(data: List[Dict[str, Any]]) -> List[InvoiceLine]:
    """
    data = [
     {
       'quantity': 1,
       'name': 'Provize',
       'unit_name': 'ks',
       'unit_price_without_vat': 100,  # cena bez DPH
       'vat_rate': 21,
     },
    ]
    """

    lines = []
    for line in data:
        lines.append(InvoiceLine(
            quantity=line.get('quantity', 1),
            name=line['name'],
            unit_name=line.get('unit_name', 'ks'),
            unit_price=line['unit_price_with_vat'],
            vat_rate=line.get('vat_rate', config.VAT_RATE),
        ))

    return lines


def create_invoice(subject_id: int,
                   lines: List[InvoiceLine],
                   proforma: bool,
                   variable_symbol: int = None,
                   custom_id: str = None) -> Invoice:
    fa = get_fakturoid_account()

    invoice = Invoice(
        custom_id=custom_id,
        # number=str(order.invoice_number),
        subject_id=subject_id,
        variable_symbol=variable_symbol,
        payment_method='bank',
        due=7,
        issued_on=datetime.date.today(),
        taxable_fulfillment_due=datetime.date.today(),
        lines=lines,
        vat_price_mode='with_vat',
        proforma=proforma,
    )
    fa.save(invoice)
    # fa.fire_invoice_event(invoice.id, 'deliver')  # pokud by chteli posilat rovnou mailem, tak odkomentuj
    return invoice


def fire_invoice_event(invoice_id, event):
    """
    :param invoice_id: int
    :param event: string
    :param fa:
    :return:
    """
    # open / sent / overdue / paid / cancelled

    # statusy faktury, ze kterých se může zavolate daná [key] eventa
    fa_statuses = {
        'pay': ['open', 'sent', 'overdue', 'cancelled'],
        'cancel': ['open', 'sent', 'overdue', 'paid'],
        'undo_cancel': ['cancelled'],
        'remove_payment': ['paid'],
        'deliver': ['open', 'sent', 'overdue', 'paid']
    }

    fa = get_fakturoid_account()

    invoice = fa.invoice(invoice_id)
    allowed_statuses = fa_statuses.get(event)
    if invoice.status in allowed_statuses:
        return fa.fire_invoice_event(invoice_id, event)
    logger.warning('cannot fire event for this invoice status', extra={'invoice_id': invoice_id,
                                                                       'event': event,
                                                                       'invoice_status': invoice.status
                                                                       })
    return


def mark_invoice_as_paid(invoice_id):
    return fire_invoice_event(invoice_id, 'pay')


def mark_invoice_as_cancelled(invoice_id):
    """
    Označí fakturu na FA jako stornovanou.
    Nepoužívejte pro účty, které jsou nastavené jako plátci DPH, nelze stornovat a vyhazuje exception.
    """
    return fire_invoice_event(invoice_id, 'cancel')


def mark_invoice_not_paid(invoice_id):
    return fire_invoice_event(invoice_id, 'remove_payment')


def mark_invoice_not_cancelled(invoice_id):
    return fire_invoice_event(invoice_id, 'undo_cancel')


def delete_invoice(invoice_id):
    fa = get_fakturoid_account()

    if invoice_id is None:
        return

    invoice = fa.invoice(invoice_id)
    fa.delete(invoice)
    return True


def _get_invoice_pdf_response(invoice_id):
    url = get_fakturoid_invoice_pdf_url(invoice_id)

    for i in range(1, 2):
        response = requests.get(url, stream=True, auth=(settings.FAKTUROID_EMAIL, settings.FAKTUROID_API_KEY))
        if response.status_code == 200:
            return response
        time.sleep(2)

    # nepodarilo se stahnout fakturu
    return None


def get_invoice_pdf_path(invoice_id, filename=None):
    response = _get_invoice_pdf_response(invoice_id)

    target_path = '/tmp/{}.pdf'.format(invoice_id if filename is None else filename)

    handle = open(target_path, "wb")
    for chunk in response.iter_content(chunk_size=512):
        if chunk:  # filter out keep-alive new chunks
            handle.write(chunk)
    return target_path


def get_invoice_private_url(invoice_id):
    fa = get_fakturoid_account()

    try:
        return fa.invoice(invoice_id).html_url
    except Exception:
        return None


def get_invoice_public_url(invoice_id):
    fa = get_fakturoid_account()

    try:
        return fa.invoice(invoice_id).public_html_url
    except Exception:
        return None


def check_invoice_status(days_back=None, status='paid'):
    if days_back is None:
        updated_since = timezone.now() - timezone.timedelta(minutes=60)
    else:
        updated_since = timezone.now() - timezone.timedelta(days=days_back)

    fa = get_fakturoid_account()

    return [{'variable_symbol': invoice.variable_symbol, 'status': invoice.status}
            for invoice in fa.invoices(proforma=False, updated_since=updated_since, status=status)]
