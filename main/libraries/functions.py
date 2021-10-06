from decimal import Decimal, ROUND_HALF_UP
import logging
import re

from django.conf import settings
from django.contrib.sites.models import Site

# Get an instance of a logger
logger = logging.getLogger('django')


def format_phone(phone):
    res = re.match(r'^(\+[0-9]{3}) ?([0-9]{3}) ?([0-9]{3}) ?([0-9]{3})$', str(phone))
    return "{} {} {} {}".format(res.group(1), res.group(2), res.group(3), res.group(4)) if res else str(phone)


def get_absolute_url(suffix=None):
    protocol = settings.ACCOUNT_DEFAULT_HTTP_PROTOCOL
    abs_url = protocol + Site.objects.get_current().domain
    if suffix is None:
        return abs_url
    else:
        return abs_url + suffix


def round_natural(f):
    return Decimal(f).quantize(0, ROUND_HALF_UP)


def xstr(s):
    return '' if s is None else str(s)
