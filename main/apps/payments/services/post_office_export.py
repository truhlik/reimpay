from typing import List, Dict, Any

from constance import config
from django.conf import settings
from django.db import models
from django.utils import timezone

from .. import constants
from main.apps.payments.managers import PaymentQuerySet
from main.apps.payments.models import PostOfficeFile
from main.libraries.utils import get_account_prefix, get_account_number, get_bank_number
from ...core.constants import PAYMENT_TYPE_POST_OFFICE
from ...studies.utils import get_payment_method_fee


class PostOfficeFileExportService(object):
    post_office_file: PostOfficeFile = None
    payments_qs: PaymentQuerySet = None
    mmdd = None  # měsíc a den vytvoření
    aa = "01"  # pořadové číslo VDS (u nás generujeme jen jeden, takže 01)

    def __init__(self, payments_qs: PaymentQuerySet):
        self.payments_qs = payments_qs
        self.mmdd = timezone.now().strftime("%m%d")

    def perform(self) -> str:
        from main.apps.post_office_order.generovani_slozenky import create_vstupni_datovy_soubor
        data = self.get_data_for_export()
        return create_vstupni_datovy_soubor(data)

    def get_data_for_export(self) -> Dict[str, List[Dict[str, Any]]]:
        return {
            "sumacni_vety": self.get_sumacni_vety(),
            "polozkove_vety": self.get_polozkove_vety(),
        }

    def get_sumacni_vety(self) -> List[Dict[str, Any]]:
        datum_platnosti = (timezone.now() + timezone.timedelta(days=25)).strftime("%Y%m%d")

        return [{
            "ID": "1",
            "DateVDS": self.mmdd,
            "SerialNumber": "{}".format(self.aa),
            "SenderNumber": "{}".format(config.POST_OFFICE_SENDER_NUMBER),
            "BankNumber": "{}".format(get_bank_number(config.BANK_ACCOUNT_CREDIT)),
            "AccountPrefix": "{}".format(get_account_prefix(config.BANK_ACCOUNT_CREDIT)),
            "AccountNumber": "{}".format(get_account_number(config.BANK_ACCOUNT_CREDIT)),
            "VariableSymbol": "{}".format(self.get_variable_symbol()),
            "ConstantSymbol": "{}".format(constants.PAYMENT_TYPE_CONSTANT_FEE_POST_OFFICE),
            "SpecificSymbol": "",
            "AmountSM": "{}".format(self.get_payments_sum_price()),
            "PriceSM": "{}".format(self.get_total_sum_price()),
            "SentenceNumber": "{}".format(len(self.payments_qs)),
            "Validity": datum_platnosti,
            "PaymentType": "1",
            "BankCodeSender": "{}".format(get_bank_number(config.BANK_ACCOUNT_OPERATIONAL)),
            "AccountPrefixSender": "{}".format(get_account_prefix(config.BANK_ACCOUNT_OPERATIONAL)),
            "AccountNumberSender": "{}".format(get_account_number(config.BANK_ACCOUNT_OPERATIONAL)),
            "ConstantSymbolSender": "{}".format(constants.PAYMENT_TYPE_CONSTANT_FEE_POST_OFFICE),
        }]

    def get_polozkove_vety(self) -> List[Dict[str, Any]]:
        i = 1
        result = []
        datum_platnosti = (timezone.now() + timezone.timedelta(days=25)).strftime("%Y%m%d")

        for payment in self.payments_qs:
            # patient_birth_date = timezone.now().strftime("%d.%m.%Y")

            # výplata pacienta v haléřích
            paycheck = round(payment.total_value * 100 / settings.INT_RATIO)

            # zjisti poplatek za platební metodu
            fee = self.get_fee_price(payment.total_value)

            # spočti celkovou částku výplata a fee
            total_paycheck = paycheck + fee

            data = {
                "ID": "1",
                "SerialNumberPV": "{}".format(i),
                "SpecificationSender": "",
                "SenderInfo": payment.name,
                "Street": payment.street,
                "HouseNumber": payment.street_number,
                "PartOfCity": "",
                "City": payment.city,
                "ZipCode": payment.zip,
                "Message": "",
                "Services": "Q",
                "PaymentDeadline": datum_platnosti,
                "AmountPV": "{}".format(paycheck),
                "PricePV": "{}".format(total_paycheck),
            }
            result.append(data)
            i += 1
        return result

    def get_payments_sum_price(self):
        """ Vrátí sumu payments v haléřích. """
        return round((self.payments_qs.aggregate(sum=models.Sum('total_value'))['sum'] or 0) * 100 / settings.INT_RATIO)

    def get_total_sum_price(self):
        """ Vrátí sumu payments a nákladů na složenky v haléřích. """
        # obojí by mělo být v haléřích
        return round(self.get_payments_sum_price() + self.get_total_fee_price())

    def get_total_fee_price(self):
        """ Vrátí sumu poplatků v haléřích. """
        return sum([self.get_fee_price(p.total_value) for p in self.payments_qs])

    def get_fee_price(self, payment_value):
        """ Vrátí poplatek za platební metodu ČP v haléřích. """
        fee = get_payment_method_fee(PAYMENT_TYPE_POST_OFFICE, payment_value)
        fee = (fee * 100) / settings.INT_RATIO  # tady už je fee v haléřích
        return round(fee)

    def get_variable_symbol(self):
        """ Vrátí variabilní symbol pro převod na ČP. """
        return "{}{}{}".format(config.POST_OFFICE_SENDER_NUMBER[2:6], self.mmdd, self.aa)
