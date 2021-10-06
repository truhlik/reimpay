from unittest.mock import patch

import pytz
import os
import json

from django.conf import settings
from django.contrib.staticfiles import finders
from django.urls import reverse
from django.utils import timezone
from django.test import TestCase
from rest_framework.test import APITestCase

from ..utils import get_list_from_smartform_response, smartform_suggestion


class CoreFunctionTests(TestCase):

    def test_get_list_from_smartform_response(self):
        json_file = open(
            os.path.join(settings.BASE_DIR, 'main', 'apps', 'smartform', 'tests', 'smartform.json'))
        data = json_file.read()
        json_file.close()
        lst = get_list_from_smartform_response(data)
        self.assertEqual(2, len(lst))
        expected_lst = [
                {
                    "street": "U Stadionu",
                    "number": "911",
                    "city": "Kralupy nad Vltavou 1",
                    "post_code": "27801"
                },
                {
                    "street": "U Stadionu",
                    "number": "911/1",
                    "city": "Beroun 1",
                    "post_code": "26601"
                }
            ]
        self.assertListEqual(expected_lst, lst)

    @patch('requests.post')
    def test_smartform_suggestion(self, mock_post):
        mock_post.return_value.status_code = 200
        json_file = open(
            os.path.join(settings.BASE_DIR, 'main', 'apps', 'smartform', 'tests', 'smartform.json'))
        data = json_file.read()
        json_file.close()
        mock_post.return_value.content = data

        resp = smartform_suggestion('test', 'test', 'test', '27801')
        # otestuju, že mi funkce vrací content
        self.assertEqual(resp, data)


class SmartFormTestCase(APITestCase):

    @patch('requests.post')
    def test_smartform_suggestion_success(self, mock_post):
        mock_post.return_value.status_code = 200
        json_file = open(
            os.path.join(settings.BASE_DIR, 'main', 'apps', 'smartform', 'tests', 'smartform.json'))
        data = json_file.read()
        json_file.close()
        mock_post.return_value.content = data

        data = {
            "street": "U Stadionu",
            "city": "Kralup",
            "post_code": "27801"
        }
        r1 = self.client.post(reverse('api-address-suggestion'), json.dumps(data), content_type='application/json')
        self.assertEqual(200, r1.status_code)
        response = {
            "results": [
                {
                    "street": "U Stadionu",
                    "number": "911",
                    "city": "Kralupy nad Vltavou 1",
                    "post_code": "27801"
                },
                {
                    "street": "U Stadionu",
                    "number": "911/1",
                    "city": "Beroun 1",
                    "post_code": "26601"
                }
            ],
        }
        self.assertEqual(response, r1.json())

    @patch('requests.post')
    def test_smartform_suggestion_failed(self, mock_post):
        mock_post.return_value.status_code = 200
        json_file = open(
            os.path.join(settings.BASE_DIR, 'main', 'apps', 'smartform', 'tests', 'smartform.json'))
        data = json_file.read()
        json_file.close()
        mock_post.return_value.content = data

        data = {
            "street": "",
            "city": "",
            "post_code": ""
        }
        r1 = self.client.post(reverse('api-address-suggestion'), json.dumps(data), content_type='application/json')
        self.assertEqual(400, r1.status_code)
