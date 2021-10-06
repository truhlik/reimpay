import logging
from typing import Tuple, Dict

from ares_util.ares import call_ares
from ares_util.validators import czech_company_id_numeric_validator

logger = logging.getLogger(__name__)


def parse_street_and_number(street_and_number: str) -> Tuple[str, str]:
    """
    Vezme jeden string (ulice a ČP dohromady) a snaží se to parsovat na dva.
    """
    for i, c in enumerate(street_and_number):
        # najdi prvni cislici v ulice_cislo
        # přeskočím první 3 písmena, abych nechytal čísla jako 1. pluku apod.
        if c.isdigit() and i not in [1, 2, 3]:
            return street_and_number[:i - 1], street_and_number[i:]

    # pokud nic nenajdu tak vrátím v ulici všechno a do ČP nic
    return street_and_number, ''


def parse_first_and_last_name(first_and_last_name: str) -> Tuple[str, str]:
    """
    Vezme jeden string (jméno a příjmení dohromady) a snaží se to parsovat na dva.
    """
    # todo fixnout problém s titulem za jménem
    try:
        return ' '.join(first_and_last_name.split()[:-1]), first_and_last_name.split()[-1]
    except IndexError:
        return first_and_last_name, ''


def get_info_from_ares(reg_number: str) -> Dict:

    if not isinstance(reg_number, str):
        try:
            reg_number = str(reg_number)
        except (ValueError, TypeError):
            return {}

    try:
        json_data = call_ares(reg_number)
    except Exception:
        return {}

    if not json_data:
        return {}

    city2_name = json_data['address']['city']
    zip = json_data['address']['zip_code']

    street2_name, number2_name = parse_street_and_number(json_data['address']['street'])

    dic = json_data['legal']['company_vat_id']
    first_name, last_name = parse_first_and_last_name(json_data['legal']['company_name'])
    full_name = json_data['legal']['company_name']

    return {
        'city': city2_name,
        'street': street2_name,
        'street_number': number2_name,
        'zip': zip,
        'vat_number': dic,
        'first_name': first_name,
        'last_name': last_name,
        'name': full_name,
    }


def validate_reg_number(reg_number: str):
    czech_company_id_numeric_validator(reg_number)


def get_location_format(number=None, street=None, zip_code=None, city=None):
    adrress = ""

    if street:
        adrress += street
        if not number and city:
            adrress += ","
        adrress += " "

    if number:
        if street:
            adrress += number
            if city:
                adrress += ", "
    if city:
        adrress += city
        # for villages without street put number after city name
        if not street and number:
            adrress += " "
            adrress += number
        if zip_code:
            adrress += " "
    if zip_code:
        adrress += zip_code
    return adrress


def get_account_prefix(bank_account_number: str) -> str:
    """ Vrátí prefix účtu z celého čísla účtu. """
    if bank_account_number.find('-') != -1:
        return bank_account_number.split('-')[0]
    return ''


def get_account_number(bank_account_number: str) -> str:
    """ Vrátí číslo účtu z celého čísla účtu. """
    return bank_account_number.split('/')[0].split('-')[-1]


def get_bank_number(bank_account_number: str) -> str:
    """ Vrátí bankovní číslo z čísla účtu. """
    return bank_account_number.split('/')[1]


def validate_bank_number(full_number: str) -> bool:
    """" Validuje číslo účtu, zda odpovídá předpisu. """

    try:
        bank_number = str(get_account_prefix(full_number) + get_account_number(full_number))
    except IndexError:
        return False
    bank_number = bank_number.zfill(16)

    try:
        bank_code = get_bank_number(full_number)
    except IndexError:
        return False

    bank_codes = [
        "0100",
        "0300",
        "0300",
        "0600",
        "0710",
        "0800",
        "2010",
        "2020",
        "2030",
        "2060",
        "2070",
        "2100",
        "2200",
        "2220",
        "2240",
        "2250",
        "2260",
        "2600",
        "2700",
        "3030",
        "3040",
        "3050",
        "3060",
        "3500",
        "4000",
        "4300",
        "5000",
        "5500",
        "5800",
        "6000",
        "6100",
        "6200",
        "6210",
        "6300",
        "6700",
        "6800",
        "7910",
        "7940",
        "7950",
        "7960",
        "7970",
        "7990",
        "8030",
        "8040",
        "8060",
        "8090",
        "8150",
        "8190",
        "8200",
        "8211",
        "8221",
        "8231",
        "8240",
        "8241",
        "8250",
    ]

    if bank_code not in bank_codes:
        return False

    # Váhy pro kontrolu základní části čísla
    base_weights = [10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2, 1]

    base_sum = 0
    i = 0
    for number in bank_number:
        base_sum += int(number) * base_weights[i]
        i += 1

    return base_sum % 11 == 0
