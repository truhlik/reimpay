from constance import config
import datetime
import logging
import requests
from fiobank import FioBank, ThrottlingError
from urllib3.exceptions import NewConnectionError

from main.apps.fiobanka.models import FiobankTransactions


logger = logging.getLogger(__name__)


class FioBankPayments:

    @staticmethod
    def start_pairing(from_date=None, to_date=None):
        if from_date is None:
            from_date = datetime.date.today()

        if to_date is None:
            to_date = datetime.date.today()

        transactions_data = []
        if getattr(config, "FIO_BANK_TOKEN"):
            client = FioBank(token=config.FIO_BANK_TOKEN)
            try:
                transactions_data += list(client.period(from_date, to_date))
            except (ThrottlingError, ValueError, requests.exceptions.HTTPError, NewConnectionError) as e:
                logger.warning('unable to contact FIO', extra={'error': e})

        if len(transactions_data) > 0:
            FioBankPayments().process_pairing(transactions_data)

    def process_pairing(self, transactions):
        transactions_list = list()
        for transaction in transactions:
            transactions_list.append(int(transaction['transaction_id']))

        transactions_database_list = list(FiobankTransactions.objects.filter(transaction_id__in=transactions_list).values_list('transaction_id', flat=True))
        if len(transactions_database_list) > 0:
            transactions = self.transactions_reformate(transactions, transactions_database_list)

        self.save_transactions(transactions)

    def transactions_reformate(self, transactions: list, transactions_database_list: list) -> list:
        """ vyhodí ty transakce, které už jsou v databázi uložené """

        to_check_list = list()
        for transaction in transactions:
            if not transaction['transaction_id'] in transactions_database_list:
                to_check_list.append(transaction)
        return to_check_list

    def save_transactions(self, transactions):
        transaction_objects_list = list()
        for transaction in transactions:
            object = FiobankTransactions()
            object.transaction_id = transaction['transaction_id']
            object.date = transaction['date']
            object.amount = transaction['amount']
            object.currency = transaction['currency']
            object.account_number = transaction['account_number']
            object.account_name = transaction['account_name']
            object.bank_code = transaction['bank_code']
            object.bank_name = transaction['bank_name']
            object.constant_symbol = transaction['constant_symbol']
            object.variable_symbol = transaction['variable_symbol']
            object.specific_symbol = transaction['specific_symbol']
            object.user_identification = transaction['user_identification']
            object.type = transaction['type']
            object.comment = transaction['comment']
            object.instruction_id = transaction['instruction_id']
            object.bic = transaction['bic']
            object.recipient_message = transaction['recipient_message']

            transaction_objects_list.append(object)

        if len(transaction_objects_list) > 0:
            FiobankTransactions.objects.bulk_create(transaction_objects_list)

