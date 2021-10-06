import datetime
import logging
import time
from typing import List, Dict, Tuple, Optional

from abo import ABO
from django.utils import timezone
from fiobank import FioBank, ThrottlingError
from requests.exceptions import HTTPError, ConnectionError, SSLError, ConnectTimeout, ReadTimeout


logger = logging.getLogger(__name__)


def create_abo_payments(payments_lst: List[Dict]) -> Optional[str]:
    """
    Vytvoří ABO soubor s předpisem plateb pro FIO
    :param payments_lst: list s platebníma údajema
    {
        'bank_account_from': '2001476165/2010',
        'bank_account_to': '1426120143/0800',
        'value': 300,
        'variable_symbol': 1234,  # voluntary
        'specific_symbol': 0,  # v případě ČP převodu není
        'constant_symbol': 610,
    }

    """

    if len(payments_lst) == 0:
        return

    logger.info('vytvářím ABO transakci')

    try:
        abo_export = ABO(
            client_account_number=payments_lst[0]['bank_account_from'],
            client_name='Reimpay',
            due_date=datetime.datetime.today())
    except ValueError as e:
        logger.error('špatně zadané platební údaje odesílatele', extra={'error': str(e)})
        return

    for payment in payments_lst:
        try:
            abo_export.add_transaction(
                payment['bank_account_to'],
                payment['value'],
                specific_symbol=payment.get('specific_symbol', 0),
                variable_symbol=payment['variable_symbol'],
                constant_symbol=payment['constant_symbol'],
            )
        except ValueError as e:
            logger.error('špatně zadané platební údaje příjemce', extra={'error': str(e)})
            return

    with open('/tmp/reimpay_import_{}.abo'.format(str(timezone.now().strftime('%y%m%d%H%M%s'))), 'w') as f:
        abo_export.save(f)

    return abo_export.get_content()


def send_abo_to_fio(abo_data: str, token: str) -> Tuple[bool, List[Dict[str, str]]]:
    """
    Odešle platby do FIO Banky ke schválení.
    :param abo_data: str, cesta k souboru s předpisem plateb ABO
    :param token: str, token pro FIO účet
    """
    if token == '' or token is None:
        return False, [{'token': 'Missing token argument'}]

    client = FioBank(token=token)
    timeout = 20

    try:
        logger.info('odesílám platby do banky')
        result = client.send("abo", "cs", 'import.abo', abo_data)
        logger.info('spojeni s bankou ukonceno: {}'.format(result['status']))

        # pokud to dopadlo dobre, tak neexistuje details a vrazim tam prazdny list
        error_lst = [] if result['status'] else result['details']
        return result['status'], error_lst
    except (HTTPError, ConnectionError, SSLError, ConnectTimeout, ReadTimeout):
        logger.error('nepodařilo se navázat spojení s bankou')
        return False, [{'connection': 'nepodařilo se navázat spojení s bankou'}]
    except IOError:
        logger.error('soubor s předpisem ABO plateb nebyl nalezen')
        return False, [{'file': 'soubor s předpisem ABO plateb nebyl nalezen'}]
    except ThrottlingError:
        logger.warning('překročen počet spojení')
        timeout += 1
        time.sleep(timeout)
        return send_abo_to_fio(abo_data, token)  # recursion
    except TypeError:
        logger.error('špatné číslo účtu')
        return False, [{'bank_account': 'špatné číslo účtu'}]
