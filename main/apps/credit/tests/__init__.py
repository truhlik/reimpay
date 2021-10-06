from django.conf import settings
from django.test import TestCase
from model_bakery import baker

from ..models import CreditBalance
from .. import utils
from .. import constants


class UtilsTestCase(TestCase):

    def setUp(self) -> None:
        super(UtilsTestCase, self).setUp()

    def test_add_credit_to_study(self):
        study = baker.make('studies.Study')
        utils.add_credit_to_study(study, 1)
        qs = CreditBalance.objects.all()
        self.assertEqual(1, len(qs))
        self.assertEqual(settings.INT_RATIO, qs[0].balance_sum)
