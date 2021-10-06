import os
import json
from django.core.management.base import BaseCommand

from django.conf import settings
from django.db import transaction

from main.apps.categories.models import Category
from main.apps.companies.models import Company
from main.apps.companies import constants
from main.apps.tags.models import Tag


class Command(BaseCommand):
    help = 'Seed Suppliers'
    # konvertováno pomocí http://beautifytools.com/excel-to-json-converter.php

    def handle(self, *args, **options):
        path = os.path.join(settings.BASE_DIR, 'seeds', 'data.json')
        with open(path, mode='r') as f:
            data = json.load(f)
            with transaction.atomic():
                self.process_data(data)

    def process_data(self, data, parent=None):
        for supplier_dct in data['Dodavatelé']:
            self._create_supplier(supplier_dct)

    def _create_supplier(self, data):
        c = Company(
            role=constants.COMPANY_ROLE_SUPPLIER,
            name=data.get('AAA', ''),
            description=data.get('Profil', None),
            email=data.get('Email', None),
            phone=data.get('Telefon', None),
            city=data.get('Město', None),
        )
        c.save()
        self.add_tags(c, data.get('Tagy - Technologie', '').split(','))
        self.add_categories(c, data.get('Tag - Kompetence', '').split(','))

    def add_tags(self, supplier, data):
        tags = []
        for tag in data:
            t = Tag.objects.filter(name=tag).first()
            if t is not None:
                tags.append(t)
        supplier.tags.set(tags)

    def add_categories(self, supplier, data):
        tags = []
        for category in data:
            t = Category.objects.filter(name=category).first()
            if t is not None:
                tags.append(t)
        supplier.categories.set(tags)
