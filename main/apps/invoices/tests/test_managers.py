from django.test import TestCase
from model_bakery import baker

from ..models import Invoice
from ...users.constants import USER_ROLE_ADMIN, USER_ROLE_CRA


class InvoicesTestCase(TestCase):

    def setUp(self) -> None:
        super(InvoicesTestCase, self).setUp()

    def test_owner_admin(self):
        company = baker.make('companies.Company')
        user = baker.make('users.User', role=USER_ROLE_ADMIN, company=company)
        i1 = baker.make('invoices.Invoice', company=user.company)
        baker.make('invoices.Invoice')
        qs = Invoice.objects.owner(user)
        self.assertEqual(1, len(qs))
        self.assertEqual(i1, qs[0])

    def test_owner_cra(self):
        company = baker.make('companies.Company')
        user = baker.make('users.User', role=USER_ROLE_CRA, company=company)
        _ = baker.make('invoices.Invoice', company=user.company)
        baker.make('invoices.Invoice')
        qs = Invoice.objects.owner(user)
        self.assertEqual(0, len(qs))

