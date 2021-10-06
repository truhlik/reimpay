from django.test import TestCase

from model_bakery import baker

from main.apps.users import constants as user_constants

from ... import constants


class SiteModelTestCase(TestCase):

    def setUp(self) -> None:
        super(SiteModelTestCase, self).setUp()

