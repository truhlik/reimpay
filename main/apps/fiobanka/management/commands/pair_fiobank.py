import datetime
from django.core.management.base import BaseCommand
from main.apps.fiobanka.functions import FioBankPayments


class Command(BaseCommand):
    help = "Default date for start and end is today."

    def add_arguments(self, parser):
        parser.add_argument('start', type=str, help='Start date for fiobank transactions', nargs='?', default=datetime.date.today())
        parser.add_argument('end', type=str, help='End date for fiobank transactions', nargs='?', default=datetime.date.today())

    def handle(self, *args, **kwargs):
        FioBankPayments.start_pairing(kwargs['start'], kwargs['end'])
