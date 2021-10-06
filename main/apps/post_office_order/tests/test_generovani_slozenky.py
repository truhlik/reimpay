import json
from unittest import TestCase
from ..generovani_slozenky import create_podaci_stvrzenka, create_vstupni_datovy_soubor
import os


class TestEqualOutputFile(TestCase):

    def test_created_vds(self):
        abs_path = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(abs_path, 'data.json')
        file = open(data_path, "r")
        data = file.read()

        data_json = json.loads(data)

        vds_path = os.path.join(abs_path, 'VDSsoubor.txt')
        file = open(vds_path, "r")
        output_vds_file = file.read()

        created_vds = create_vstupni_datovy_soubor(data_json)

        self.assertEqual(output_vds_file, created_vds)

    def test_created_pds(self):
        abs_path = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(abs_path, 'data.json')
        file = open(data_path, "r")
        data = file.read()

        data_json = json.loads(data)

        pds_path = os.path.join(abs_path, 'PDSsoubor.txt')
        pds_file = open(pds_path, "r")
        output_pds_file = pds_file.read()

        created_pds = create_podaci_stvrzenka(data_json)

        self.assertEqual(output_pds_file, created_pds)
