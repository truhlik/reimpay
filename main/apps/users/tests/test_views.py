from allauth.account.models import EmailAddress
from django.core import mail
from django.test import Client
from django.urls import reverse

from model_bakery import baker
from rest_framework.test import APITestCase

from main.apps.users.models import User
from .. import constants


class UserSerializersTestCase(APITestCase):

    def setUp(self) -> None:
        super(UserSerializersTestCase, self).setUp()

    def do_auth(self):
        self.client.force_authenticate(user=self.user)

    # fixme login test view
    # def test_login_view(self):
    #     client = Client()
    #     user = baker.make('users.User', email='test@test.cz', is_active=True)
    #     user.set_password('test1324')
    #
    #     url = reverse('rest_login')
    #     resp = client.post(url, {'email': 'test@test.cz', 'password': 'test1324'}, content_type='application/json')
    #     self.assertEqual(200, resp.status_code)
    #     self.assertTrue('key' in resp.json())

    def test_self_view_get(self):
        c = baker.make('companies.Company')
        self.user = baker.make('users.User', role=constants.USER_ROLE_CRA, company=c)
        self.do_auth()
        r = self.client.get(reverse('user-self'))
        self.assertEqual(200, r.status_code)
        self.assertEqual(str(self.user.id), r.json()['id'])

    def test_self_view_patch(self):
        c = baker.make('companies.Company')
        self.user = baker.make('users.User', first_name='Luboš', last_name='Truhlář', role=constants.USER_ROLE_CRA, company=c)
        self.do_auth()
        r = self.client.patch(reverse('user-self'), {'first_name': 'test1',
                                                     'last_name': 'test2',
                                                     })
        self.assertEqual(200, r.status_code)
        self.assertEqual(
            ['test1', 'test2'],
            [r.json()['first_name'], r.json()['last_name']]
        )

    def test_create_by_admin(self):
        c = baker.make('companies.Company')
        self.user = baker.make('users.User', role=constants.USER_ROLE_ADMIN, company=c)
        self.do_auth()
        r = self.client.post(reverse('user-list'), {'first_name': 'test1',
                                                    'last_name': 'test2',
                                                    'email': 'lubos@test.cz',
                                                    'role': constants.USER_ROLE_ADMIN,
                                                    })
        self.assertEqual(201, r.status_code)
        qs = User.objects.all()
        self.assertEqual(2, len(qs))
        self.assertEqual(self.user.company, qs[0].company)

    def test_create_by_cra_fail(self):
        c = baker.make('companies.Company')
        self.user = baker.make('users.User', role=constants.USER_ROLE_CRA, company=c)
        self.do_auth()
        r = self.client.post(reverse('user-list'), {'first_name': 'test1',
                                                    'last_name': 'test2',
                                                    'email': 'lubos@test.cz',
                                                    'role': constants.USER_ROLE_ADMIN,
                                                    })
        self.assertEqual(403, r.status_code)

    def test_create_send_reset_email(self):
        c = baker.make('companies.Company')
        self.user = baker.make('users.User', role=constants.USER_ROLE_ADMIN, company=c)
        self.do_auth()
        r = self.client.post(reverse('user-list'), {'first_name': 'test1',
                                                    'last_name': 'test2',
                                                    'email': 'lubos@test.cz',
                                                    'role': constants.USER_ROLE_ADMIN,
                                                    })
        self.assertEqual(201, r.status_code)
        self.assertEqual(1, len(mail.outbox))
        self.assertEqual('Reimpay account created', mail.outbox[0].subject)

    def test_list_view(self):
        c = baker.make('companies.Company')
        self.user = baker.make('users.User', role=constants.USER_ROLE_ADMIN, company=c)
        _ = baker.make('users.User', role=constants.USER_ROLE_ADMIN, company=c, is_active=False)
        baker.make('users.User', role=constants.USER_ROLE_CRA)
        self.do_auth()
        r = self.client.get(reverse('user-list'))
        self.assertEqual(200, r.status_code)
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(str(self.user.id), r.data['results'][0]['id'])

    def test_list_view_search_role_by_cra(self):
        c = baker.make('companies.Company')
        self.user = baker.make('users.User', role=constants.USER_ROLE_CRA, company=c)
        user_admin = baker.make('users.User', role=constants.USER_ROLE_ADMIN, company=c)
        baker.make('users.User', role=constants.USER_ROLE_CRA)
        self.do_auth()
        r = self.client.get(reverse('user-list') + '?role={}'.format(constants.USER_ROLE_ADMIN))
        self.assertEqual(200, r.status_code)
        self.assertEqual(0, r.data['pagination']['count'])

    def test_list_view_search_role_by_admin(self):
        c = baker.make('companies.Company')
        user_cra = baker.make('users.User', role=constants.USER_ROLE_CRA, company=c)
        self.user = baker.make('users.User', role=constants.USER_ROLE_ADMIN, company=c)
        baker.make('users.User', role=constants.USER_ROLE_CRA)
        self.do_auth()
        r = self.client.get(reverse('user-list') + '?role={}'.format(constants.USER_ROLE_ADMIN))
        self.assertEqual(200, r.status_code)
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(str(self.user.id), r.data['results'][0]['id'])

    def test_list_view_search_study_id(self):
        c = baker.make('companies.Company')
        self.user = baker.make('users.User', role=constants.USER_ROLE_ADMIN, company=c)
        user2 = baker.make('users.User', role=constants.USER_ROLE_CRA, company=c)

        study = baker.make('studies.Study', company=c)
        baker.make('studies.Site', cra=self.user, study=study)

        study2 = baker.make('studies.Study', company=c)
        baker.make('studies.Site', cra=user2, study=study2)

        baker.make('users.User', role=constants.USER_ROLE_CRA)
        self.do_auth()
        r = self.client.get(reverse('user-list') + '?study_id={}'.format(study.id))
        self.assertEqual(200, r.status_code)
        self.assertEqual(1, r.data['pagination']['count'])
        self.assertEqual(str(self.user.id), r.data['results'][0]['id'])

    def test_self_view_delete(self):
        c = baker.make('companies.Company')
        self.user = baker.make('users.User', first_name='Luboš', last_name='Truhlář', role=constants.USER_ROLE_CRA, company=c)
        self.do_auth()
        r = self.client.delete(reverse('user-self'))
        self.assertEqual(204, r.status_code)

    def test_delete(self):
        c = baker.make('companies.Company')
        self.user = baker.make('users.User', first_name='Luboš', last_name='Truhlář', role=constants.USER_ROLE_CRA, company=c)
        self.do_auth()
        r = self.client.delete(reverse('user-detail', args=(self.user.id, )))
        self.assertEqual(204, r.status_code)
