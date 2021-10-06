from constance import config
from django.conf import settings
from django.utils import timezone

from django.test import TestCase
from model_bakery import baker

from .. import constants
from ..models import Payment
from ..services.post_office_export import PostOfficeFileExportService


class PostOfficeFileExportServiceTestCase(TestCase):

    def setUp(self) -> None:
        self.maxDiff = None
        super(PostOfficeFileExportServiceTestCase, self).setUp()
        config.POST_OFFICE_FEE = 4500
        study = baker.make('studies.Study', variable_symbol=123456)
        p1 = baker.make('payments.Payment',
                        study=study,
                        total_value=2 * settings.INT_RATIO,
                        bank_account_from='1',
                        bank_account_to='2',
                        variable_symbol=study.variable_symbol,
                        specific_symbol=1,
                        constant_symbol=constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_POST_OFFICE,
                        name='name1',
                        street='street1',
                        street_number='1',
                        city='city1',
                        zip='zip1',
                        )
        p2 = baker.make('payments.Payment',
                        study=study,
                        total_value=3 * settings.INT_RATIO,
                        bank_account_from='1',
                        bank_account_to='2',
                        variable_symbol=study.variable_symbol,
                        specific_symbol=1,
                        constant_symbol=constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_POST_OFFICE,
                        name='name2',
                        street='street2',
                        street_number='2',
                        city='city2',
                        zip='zip2',
                        )
        p3 = baker.make('payments.Payment',
                        study=study,
                        total_value=4 * settings.INT_RATIO,
                        bank_account_from='1',
                        bank_account_to='2',
                        variable_symbol=study.variable_symbol,
                        specific_symbol=3,
                        constant_symbol=constants.PAYMENT_TYPE_CONSTANT_PAYCHECK_POST_OFFICE,
                        name='name3',
                        street='street3',
                        street_number='3',
                        city='city3',
                        zip='zip3',
                        )
        payments_qs = Payment.objects.paychecks()
        self.svc = PostOfficeFileExportService(payments_qs)

    def test_get_payments_sum_price(self):
        self.assertEqual(900, self.svc.get_payments_sum_price())

    def test_get_total_sum_price(self):
        self.assertEqual(900 + 3 * 4500, self.svc.get_total_sum_price())

    def test_get_fee_price(self):
        self.assertEqual(4500, self.svc.get_fee_price(100 * settings.INT_RATIO))

    def test_get_fee_price_2(self):
        self.assertEqual(5300, self.svc.get_fee_price(10000 * settings.INT_RATIO))

    def test_get_sumacni_vety(self):
        config.POST_OFFICE_SENDER_NUMBER = "654321"
        config.BANK_ACCOUNT_CREDIT = "000111-123456789/0800"
        config.BANK_ACCOUNT_OPERATIONAL = "777123456/0100"
        mmdd = timezone.now().strftime("%m%d")
        yyyymmdd = (timezone.now() + timezone.timedelta(days=25)).strftime("%Y%m%d")

        sv_lst = self.svc.get_sumacni_vety()
        exp_lst = [
            {
                "ID": "1",
                "DateVDS": timezone.now().strftime("%m%d"),
                "SerialNumber": "01",
                "SenderNumber": "654321",
                "BankNumber": "0800",
                "AccountPrefix": "000111",
                "AccountNumber": "123456789",
                "VariableSymbol": "4321{}01".format(mmdd),
                "ConstantSymbol": "710",
                "SpecificSymbol": "",
                "AmountSM": "900",
                "PriceSM": "14400",
                "SentenceNumber": "3",
                "Validity": yyyymmdd,
                "PaymentType": "1",
                "BankCodeSender": "0100",
                "AccountPrefixSender": "",
                "AccountNumberSender": "777123456",
                "ConstantSymbolSender": "710",
            }
        ]
        self.assertEqual(exp_lst, sv_lst)

    def test_get_polozkove_vety(self):
        config.POST_OFFICE_SENDER_NUMBER = "654321"
        config.BANK_ACCOUNT_CREDIT = "000111-123456789/0800"
        mmdd = timezone.now().strftime("%m%d")
        yyyymmdd = (timezone.now() + timezone.timedelta(days=25)).strftime("%Y%m%d")

        sv_lst = self.svc.get_polozkove_vety()
        exp_lst = [
            {
                "ID": "1",
                "SerialNumberPV": "1",
                "SpecificationSender": "",  # timezone.now().strftime("%d.%m.%Y")
                "SenderInfo": 'name1',
                "Street": 'street1',
                "HouseNumber": '1',
                "PartOfCity": "",
                "City": 'city1',
                "ZipCode": 'zip1',
                "Message": "",
                "Services": "Q",
                "PaymentDeadline": yyyymmdd,
                "AmountPV": "200",
                "PricePV": "4700",
            },
            {
                "ID": "1",
                "SerialNumberPV": "2",
                "SpecificationSender": "",  # timezone.now().strftime("%d.%m.%Y")
                "SenderInfo": 'name2',
                "Street": 'street2',
                "HouseNumber": '2',
                "PartOfCity": "",
                "City": 'city2',
                "ZipCode": 'zip2',
                "Message": "",
                "Services": "Q",
                "PaymentDeadline": yyyymmdd,
                "AmountPV": "300",
                "PricePV": "4800",
            },
            {
                "ID": "1",
                "SerialNumberPV": "3",
                "SpecificationSender": "",  # timezone.now().strftime("%d.%m.%Y")
                "SenderInfo": 'name3',
                "Street": 'street3',
                "HouseNumber": '3',
                "PartOfCity": "",
                "City": 'city3',
                "ZipCode": 'zip3',
                "Message": "",
                "Services": "Q",
                "PaymentDeadline": yyyymmdd,
                "AmountPV": "400",
                "PricePV": "4900",
            },

        ]
        self.assertEqual(exp_lst, sv_lst)