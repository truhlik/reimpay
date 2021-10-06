import random

from main.apps.studies.models import Site


def generate_site_pin() -> str:
    already_exists = True
    pin = None
    while already_exists:
        pin = random.randint(10000, 99999)
        already_exists = Site.objects.filter(pin=pin).exists()
    return str(pin)
