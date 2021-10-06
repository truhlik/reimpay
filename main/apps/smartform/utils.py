import requests
import logging
import json

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


logger = logging.getLogger(__name__)


def smartform_suggestion(street, number, city, zip_code, suggesting_field=None):
    if settings.SMARTFORM_API_KEY in ['', None]:
        raise ImproperlyConfigured('SMARTFORM_API_KEY is not defined')

    fields = {
        'street': 'STREET',
        'number': 'STREET_AND_NUMBER',
        'city': 'CITY',
        'zip': 'ZIP',
        '': 'WHOLE_ADDRESS'
    }

    data = {'password': settings.SMARTFORM_API_KEY,
            'values': {
                # 'STREET': street,
                # 'NUMBER': number,
                # 'CITY': city,
                # 'ZIP': zip_code,
                # 'COUNTRY': 'CZ',
                'WHOLE_ADDRESS': '{}, {}, {}'.format(street, city, zip_code)
            },
            'limit': 10,
            'fieldType': fields.get(suggesting_field, 'WHOLE_ADDRESS'),
            }

    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

    try:
        resp = requests.post(settings.SMARTFORM_URL, json=data, headers=headers)
    except requests.exceptions.RequestException as e:
        logger.warning('Problem with Smartform address suggestion.', extra={'error': str(e)})
        return None

    if resp.status_code != 200:
        logger.warning('Problem with Smartform address suggestion.', extra={'status_code': resp.status_code})
        return None

    return resp.content


def get_list_from_smartform_response(text):
    try:
        smartform_dct = json.loads(text)
    except json.JSONDecodeError:
        logger.warning('Given text is not JSON serializable.')
        return []

    suggestion_lst = smartform_dct.get('suggestions', []) or []
    result_lst = []
    for item in suggestion_lst:
        try:
            result_lst.append({
                "street": item['values'].get('STREET', ''),
                "number": item['values'].get('NUMBER', ''),
                "city": item['values'].get('CITY', ''),
                "post_code": item['values'].get('ZIP', ''),
            })
        except KeyError:
            continue
    return result_lst
