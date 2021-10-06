from django.test import TestCase
from django.utils import timezone

from model_bakery import baker
from requests import Request

from main.apps.core.constants import PAYMENT_TYPE_BANK_TRANSFER, PAYMENT_TYPE_POST_OFFICE
from main.apps.users import constants as user_constants

from ... import serializers, utils
from ...constants import STUDY_VISIT_TYPE_UNSCHEDULED, STUDY_STATUS_PROGRESS
from ...models import Visit


class PatientSerializerTestCase(TestCase):

    def setUp(self) -> None:
        super(PatientSerializerTestCase, self).setUp()

    def test_detail_serializer(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)

        arm = baker.make('studies.Arm', study=study1)
        utils.create_visits(study1, arm)
        site = baker.make('studies.Site', study=study1)
        patient1 = baker.make('studies.Patient', arm=arm, site=site, study=study1)
        pv = baker.make('studies.PatientVisit', patient=patient1, visit=Visit.objects.regular().first())
        pvi = baker.make('studies.PatientVisitItem', patient_visit=pv)
        baker.make('studies.PatientVisitItem', patient_visit=pv)

        request = Request()
        request.user = user

        serializer = serializers.PatientDetailSerializer(patient1, context={'request': request})
        self.assertEqual(
            ['id', 'arm', 'number', 'payment_type', 'payment_info', 'arm_name', 'visits', 'paid', 'site',
             'next_visits', 'study_obj', 'patient_visit_items', 'unscheduled_left'],
            list(serializer.data.keys())
        )
        self.assertEqual(2, len(serializer.data['patient_visit_items']))
        self.assertEqual(
            ['payment', 'visit', 'date', 'amount', 'note', 'payment_status', 'reject_reason',],
            list(serializer.data['patient_visit_items'][0].keys())
        )

    def test_unscheduled_visits_left(self):
        request = Request()

        arm = baker.make('studies.Arm', max_unscheduled=0)
        patient = baker.make('studies.Patient', arm=arm)
        visit = baker.make('studies.Visit', arm=arm, visit_type=STUDY_VISIT_TYPE_UNSCHEDULED, number=2)
        pv = baker.make('studies.PatientVisit', patient=patient, visit=visit)
        qs = utils.get_unscheduled_visits(patient)
        self.assertEqual(1, len(qs))
        self.assertEqual(pv, qs[0])

        serializer = serializers.PatientDetailSerializer(patient, context={'request': request})
        self.assertEqual(1, serializer.data['unscheduled_left'])

    def test_instance_serialization(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c, bank_transfer=True, post_office_cash=True)

        study2 = baker.make('studies.Study', company=c)
        arm = baker.make('studies.Arm', study=study1)
        site = baker.make('studies.Site', study=study1)  # site from other company
        patient1 = baker.make('studies.Patient', arm=arm, site=site, study=study1, number='test123',
                              payment_info='test', name='test', street='test', city='test', zip='test')

        request = Request()
        request.user = user

        serializer = serializers.PatientBaseSerializer(patient1, context={'request': request})
        self.assertEqual("", serializer.data['payment_info'])
        self.assertEqual("", serializer.data['name'])
        self.assertEqual("", serializer.data['street'])
        self.assertEqual("", serializer.data['city'])
        self.assertEqual("", serializer.data['zip'])

    def test_validation_success(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)
        study1 = baker.make('studies.Study', company=c, bank_transfer=True, status=STUDY_STATUS_PROGRESS)

        arm = baker.make('studies.Arm', study=study1)
        site = baker.make('studies.Site', study=study1, cra=user)

        request = Request()
        request.user = user

        serializer = serializers.PatientBaseSerializer(data={
            'number': 'test',
            'payment_type': PAYMENT_TYPE_BANK_TRANSFER,
            'payment_info': '7998862/0800',
            'arm': arm.id,
            'site': site.id,
        },
            context={'request': request})
        self.assertTrue(serializer.is_valid())

    def test_validation_study_failed(self):
        c = baker.make('companies.Company')
        c2 = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c2)
        request = Request()
        request.user = user

        study1 = baker.make('studies.Study', company=c)


        study2 = baker.make('studies.Study', company=c2)


        arm = baker.make('studies.Arm', study=study1)
        site = baker.make('studies.Site', study=study2)
        # arm.study and site.study does not match

        serializer = serializers.PatientBaseSerializer(data={
            'number': 'test123',
            'payment_type': PAYMENT_TYPE_BANK_TRANSFER,
            'payment_info': '7998862/0800',
            'arm': arm.id,
            'site': site.id,
        },
            context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(1, len(serializer.errors))
        self.assertTrue('arm' in serializer.errors.keys())

    def test_save(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c, bank_transfer=True, status=STUDY_STATUS_PROGRESS)


        request = Request()
        request.user = user
        arm = baker.make('studies.Arm', study=study1)
        site = baker.make('studies.Site', study=study1)

        data = {
            'number': 'test123',
            'payment_type': PAYMENT_TYPE_BANK_TRANSFER,
            'payment_info': '7998862/0800',
            'arm': arm.id,
            'site': site.id,
        }
        serializer = serializers.PatientBaseSerializer(data=data,
                                                       context={'request': request})
        serializer.is_valid()
        instance = serializer.save()
        exp_data = {
            'number': 'test123',
            'payment_type': PAYMENT_TYPE_BANK_TRANSFER,
            'payment_info': '7998862/0800',
            'arm': arm.id,
            'site': site.id,
            'change_payment_request': None,
        }
        saved_data = {
            'number': instance.number,
            'payment_type': instance.payment_type,
            'payment_info': instance.payment_info,
            'arm': instance.arm_id,
            'site': instance.site_id,
            'change_payment_request': instance.change_payment_request.date() if instance.change_payment_request else None,
        }
        self.assertEqual(
            exp_data,
            saved_data,
        )

    def test_validate_arm_failed(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)

        study2 = baker.make('studies.Study', company=c)
        arm = baker.make('studies.Arm')  # arm from other company
        site = baker.make('studies.Site', study=study1)

        request = Request()
        request.user = user

        serializer = serializers.PatientBaseSerializer(data={
            'number': 'test123',
            'payment_type': PAYMENT_TYPE_BANK_TRANSFER,
            'payment_info': '7998862/0800',
            'arm': arm.id,
            'site': site.id,
        },
            context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(1, len(serializer.errors))
        self.assertTrue('arm' in serializer.errors.keys())

    def test_validate_site_cra_other_site(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)
        study1 = baker.make('studies.Study', company=c)
        _ = baker.make('studies.Site', study=study1, cra=user)

        arm = baker.make('studies.Arm', study=study1)
        site = baker.make('studies.Site', study=study1)  # CRA is not defined

        request = Request()
        request.user = user

        serializer = serializers.PatientBaseSerializer(data={
            'number': 'test123',
            'payment_type': PAYMENT_TYPE_BANK_TRANSFER,
            'payment_info': '7998862/0800',
            'arm': arm.id,
            'site': site.id,
        },
            context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(1, len(serializer.errors))
        self.assertTrue('site' in serializer.errors.keys())

    def test_validate_site_failed(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c)

        study2 = baker.make('studies.Study', company=c)
        arm = baker.make('studies.Arm', study=study1)
        site = baker.make('studies.Site')  # site from other company

        request = Request()
        request.user = user

        serializer = serializers.PatientBaseSerializer(data={
            'number': 'test123',
            'payment_type': PAYMENT_TYPE_BANK_TRANSFER,
            'payment_info': '7998862/0800',
            'arm': arm.id,
            'site': site.id,
        },
            context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(1, len(serializer.errors))
        self.assertTrue('site' in serializer.errors.keys())

    def test_validate_payment_type_failed(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c, bank_transfer=True, post_office_cash=False, status=STUDY_STATUS_PROGRESS)

        study2 = baker.make('studies.Study', company=c)
        arm = baker.make('studies.Arm', study=study1)
        site = baker.make('studies.Site', study=study1)  # site from other company

        request = Request()
        request.user = user

        serializer = serializers.PatientBaseSerializer(data={
            'number': 'test123',
            'payment_type': PAYMENT_TYPE_POST_OFFICE,
            'payment_info': '7998862/0800',
            'arm': arm.id,
            'site': site.id,
        },
            context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(1, len(serializer.errors))
        self.assertTrue('payment_type' in serializer.errors.keys())

    def test_validate_number(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c, bank_transfer=True, post_office_cash=True, status=STUDY_STATUS_PROGRESS)

        study2 = baker.make('studies.Study', company=c)
        arm = baker.make('studies.Arm', study=study1)
        site = baker.make('studies.Site', study=study1)  # site from other company
        patient1 = baker.make('studies.Patient', arm=arm, site=site, study=study1, number='test123')

        request = Request()
        request.user = user

        serializer = serializers.PatientBaseSerializer(data={
            'number': 'test123',
            'payment_type': PAYMENT_TYPE_POST_OFFICE,
            'payment_info': '7998862/0800',
            'arm': arm.id,
            'site': site.id,
            'name': 'a',
            'street': 'b',
            'street_number': 'c',
            'city': 'd',
            'zip': 'e',
        },
            context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(1, len(serializer.errors))
        self.assertTrue('number' in serializer.errors.keys())

    def test_validate_payment_info(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c, bank_transfer=True, post_office_cash=True, status=STUDY_STATUS_PROGRESS)

        study2 = baker.make('studies.Study', company=c)
        arm = baker.make('studies.Arm', study=study1)
        site = baker.make('studies.Site', study=study1)  # site from other company
        patient1 = baker.make('studies.Patient', arm=arm, site=site, study=study1, number='test123')

        request = Request()
        request.user = user

        serializer = serializers.PatientBaseSerializer(data={
            'number': 'test123',
            'payment_type': PAYMENT_TYPE_BANK_TRANSFER,
            'payment_info': '7998861/0800',
            'arm': arm.id,
            'site': site.id,
        },
            context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(1, len(serializer.errors))
        self.assertTrue('payment_info' in serializer.errors.keys())

    def test_validate_change_arm(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c, bank_transfer=True, post_office_cash=True)

        study2 = baker.make('studies.Study', company=c)
        arm = baker.make('studies.Arm', study=study1)
        arm2 = baker.make('studies.Arm', study=study1)
        site = baker.make('studies.Site', study=study1)  # site from other company
        patient1 = baker.make('studies.Patient', arm=arm, site=site, study=study1, number='test123')

        request = Request()
        request.user = user

        serializer = serializers.PatientBaseSerializer(patient1, data={
            'arm': arm2.id,
        }, context={'request': request}, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(1, len(serializer.errors))
        self.assertTrue('arm' in serializer.errors.keys())

    def test_validate_change_number(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c, bank_transfer=True, post_office_cash=True)

        study2 = baker.make('studies.Study', company=c)
        arm = baker.make('studies.Arm', study=study1)
        arm2 = baker.make('studies.Arm', study=study1)
        site = baker.make('studies.Site', study=study1)  # site from other company
        patient1 = baker.make('studies.Patient', arm=arm, site=site, study=study1, number='test123')

        request = Request()
        request.user = user

        serializer = serializers.PatientBaseSerializer(patient1, data={
            'number': '321test',
        }, context={'request': request}, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(1, len(serializer.errors))
        self.assertTrue('number' in serializer.errors.keys())

    def test_validate_change_without_number(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c, bank_transfer=True, post_office_cash=True)

        study2 = baker.make('studies.Study', company=c)
        arm = baker.make('studies.Arm', study=study1)
        arm2 = baker.make('studies.Arm', study=study1)
        site = baker.make('studies.Site', study=study1)  # site from other company
        patient1 = baker.make('studies.Patient', arm=arm, site=site, study=study1, number='test123')

        request = Request()
        request.user = user

        serializer = serializers.PatientBaseSerializer(patient1, data={
            'street_number': '321test',
        }, context={'request': request}, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertEqual(1, len(serializer.errors))
        self.assertTrue('number' in serializer.errors.keys())

    def test_validate_change_to_post_without_account_success(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c, bank_transfer=True, post_office_cash=True)


        patient1 = baker.make('studies.Patient', payment_type=PAYMENT_TYPE_BANK_TRANSFER, payment_info='7998862/0800', study=study1)

        request = Request()
        request.user = user

        serializer = serializers.PatientBaseSerializer(patient1, data={
            'payment_info': '',
            'payment_type': PAYMENT_TYPE_POST_OFFICE,
            'number': patient1.number,
            'name': 'a',
            'street': 'b',
            'street_number': 'c',
            'city': 'd',
            'zip': 'e',
        }, context={'request': request}, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(0, len(serializer.errors))

    def test_validate_change_to_bank_without_address_success(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c, bank_transfer=True, post_office_cash=True)


        patient1 = baker.make('studies.Patient', payment_type=PAYMENT_TYPE_POST_OFFICE, study=study1)

        request = Request()
        request.user = user

        serializer = serializers.PatientBaseSerializer(patient1, data={
            'payment_info': '7998862/0800',
            'payment_type': PAYMENT_TYPE_BANK_TRANSFER,
            'number': patient1.number,
            'name': None,
            'street': None,
            'street_number': None,
            'city': None,
            'zip': None,
        }, context={'request': request}, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(0, len(serializer.errors))

    def test_validate_number_not_required_for_doctor(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        study1 = baker.make('studies.Study', company=c, bank_transfer=True, post_office_cash=True)


        patient1 = baker.make('studies.Patient', payment_type=PAYMENT_TYPE_POST_OFFICE, study=study1)

        request = Request()
        request.user = user

        serializer = serializers.PatientBaseSerializer(patient1, data={
            'change_payment_request': True,
        }, context={'request': request}, partial=True)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(0, len(serializer.errors))
