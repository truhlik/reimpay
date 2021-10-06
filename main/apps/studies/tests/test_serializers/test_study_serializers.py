from django.conf import settings
from django.test import TestCase
from django.utils import timezone

from model_bakery import baker
from requests import Request

from main.apps.credit.constants import CREDIT_BALANCE_COMMISSION, CREDIT_BALANCE_TOPUP
from main.apps.studies.models import Arm, Visit
from main.apps.users import constants as user_constants

from ... import constants
from ... import serializers
from ...serializers import StudyReadSerializer, StudyWriteSerializer


class StudySerializerTestCase(TestCase):

    def setUp(self) -> None:
        super(StudySerializerTestCase, self).setUp()

    def test_keys(self):
        s = baker.make('studies.Study')
        serializer = StudyReadSerializer(s)
        self.assertEqual(
            [
                'id',
                'status',

                'number',
                'identifier',
                'notes',
                'bank_transfer',
                'post_office_cash',
                'pay_frequency',
                'operator',
                'sponsor_name',
                'bank_account',

                'active_patients',
                'paid',
                'credit',
                'date_launched',
                'date_last_visit',
            ],
            list(serializer.data.keys())
        )

    def test_values_paid(self):
        study = baker.make('studies.Study')
        _ = baker.make('credit.Creditbalance', balance_type=CREDIT_BALANCE_COMMISSION, study=study, balance_amount=-1000 * settings.INT_RATIO)
        serializer = StudyReadSerializer(study)
        self.assertEqual(1000, serializer.data['paid'])

    def test_values_credit(self):
        study = baker.make('studies.Study')
        _ = baker.make('credit.Creditbalance', balance_type=CREDIT_BALANCE_TOPUP, study=study, balance_amount=1000 * settings.INT_RATIO)
        serializer = StudyReadSerializer(study)
        self.assertEqual(1000, serializer.data['credit'])

    def test_values_date_launched(self):
        study = baker.make('studies.Study')
        study.status = constants.STUDY_STATUS_PROGRESS
        study.save()
        serializer = StudyReadSerializer(study)
        now = timezone.now()
        self.assertEqual(now.strftime("%Y-%m-%d"), serializer.data['date_launched'])

    def test_validate_success(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)

        request = Request()
        request.user = user

        study1 = baker.make('studies.Study', company=c)

        serializer = serializers.StudyWriteSerializer(data={
            'number': 1,
            'identifier': 'test',
            'notes': 'test',
            'bank_transfer': True,
            'post_office_cash': True,
            'pay_frequency': 2,
            'bank_account': '7998862/0800',
        },
            context={'request': request})
        self.assertTrue(serializer.is_valid())

    def test_validate_account_number(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)

        request = Request()
        request.user = user

        study1 = baker.make('studies.Study', company=c)

        serializer = serializers.StudyWriteSerializer(data={
            'number': 1,
            'identifier': 'test',
            'notes': 'test',
            'bank_transfer': True,
            'post_office_cash': True,
            'pay_frequency': 2,
            'bank_account': '7998861/0800'
        },
            context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertEqual(1, len(serializer.errors))
        self.assertTrue('bank_account' in serializer.errors.keys())

    def test_validate_users_other_company_user_selected(self):
        c = baker.make('companies.Company')
        c2 = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        user2 = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c2)

        request = Request()
        request.user = user

        serializer = serializers.StudyWriteSerializer(data={
            'number': 1,
            'identifier': 'test',
            'notes': 'test',
            'bank_transfer': True,
            'post_office_cash': True,
            'pay_frequency': 2,
            'users': [{'id': str(user2.id)}],
            'bank_account': '7998862/0800',
        },
            context={'request': request})
        # serializer je validní i když tam posílám špatný users, protože on je ignoruje
        self.assertTrue(serializer.is_valid())

    def test_check_base_visit_map_created(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        user2 = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)

        request = Request()
        request.user = user

        study1 = baker.make('studies.Study', company=c)

        serializer = serializers.StudyWriteSerializer(data={
            'number': 1,
            'identifier': 'test',
            'notes': 'test',
            'bank_transfer': True,
            'post_office_cash': True,
            'pay_frequency': 2,
            'users': [{'id': user2.id}],
            'bank_account': '7998862/0800',
        },
            context={'request': request})
        if not serializer.is_valid():
            print(serializer.errors)

        study = serializer.save(company=c)
        self.assertEqual(1, Arm.objects.filter(study=study).count())
        self.assertEqual(3, Visit.objects.filter(study=study).count())

    def test_validate_without_any_change(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        cra = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)

        request = Request()
        request.user = user

        study1 = baker.make('studies.Study',
                            company=c,
                            bank_transfer=True,
                            status=constants.STUDY_STATUS_DRAFT,
                            number=1, identifier='test')

        serializer = serializers.StudyWriteSerializer(study1, data={

        }, partial=True, context={'request': request})
        self.assertTrue(serializer.is_valid())

    def test_save(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        cra = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)
        cra2 = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)

        request = Request()
        request.user = user

        study1 = baker.make('studies.Study',
                            company=c,
                            bank_transfer=True,
                            status=constants.STUDY_STATUS_DRAFT,
                            number='1', identifier='test')

        serializer = serializers.StudyWriteSerializer(study1, data={
            "number": '2',
        }, partial=True, context={'request': request})
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEqual('2', instance.number)

    def test_save_partial_wihout_change(self):
        c = baker.make('companies.Company')
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        cra = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)
        cra2 = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)

        request = Request()
        request.user = user

        study1 = baker.make('studies.Study',
                            company=c,
                            bank_transfer=True,
                            status=constants.STUDY_STATUS_DRAFT,
                            number=1, identifier='test')

        serializer = serializers.StudyWriteSerializer(study1, data={
        }, partial=True, context={'request': request})
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEqual(constants.STUDY_STATUS_DRAFT, instance.status)
        self.assertEqual(1, instance.number)

    def test_save_with_company_and_comission(self):
        c = baker.make('companies.Company', commission=5)
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        u2 = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)
        request = Request()
        request.user = user

        serializer = serializers.StudyWriteSerializer(data={
            'number': 1,
            'identifier': 'test',
            'notes': 'test',
            'bank_transfer': True,
            'post_office_cash': True,
            'pay_frequency': 2,
            'users': [{'id': u2.id}],
            'bank_account': '7998862/0800',
        },
            context={'request': request})
        if not serializer.is_valid():
            print(serializer.errors)
        instance = serializer.save()
        self.assertEqual(c, instance.company)
        self.assertTrue(5, instance.commission)
        self.assertIsNotNone(instance.variable_symbol)

    def test_notes_length_gt_1000(self):
        c = baker.make('companies.Company', commission=5)
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        u2 = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)
        request = Request()
        request.user = user

        serializer = serializers.StudyWriteSerializer(data={
            'number': 1,
            'identifier': 'test',
            'notes': "Dejte agentuře do smlouvy, že jí zaplatíte jen když se váš konverzní poměr zvedne o X, a agentura"
                     "se nebude soustředit na nic jiného, než na váš konverzní poměr. V té chvíli nesedíte na stejné "
                     "straně stolu — místo partnerství vytěžujete svůj nový zdroj, tedy agenturu. "
                     "Agentura chce dostat zaplaceno a když chcete vyšší konverze, dostanete vyšší konverze. "
                     "Nejjednodušší způsob, jak zvýšit konverze je odbourat návštěvnost, která nekonvertuje. Říkejme "
                     "tomu třeba optimalizace kvality návštěvnosti. Něco zakážete v robots.txt, něco smažete a "
                     "konverze jsou najednou 2%. Kliente plať. "
                     "Druhá nejjednodušší možnost je sleva. Masivní slevová kampaň, všechno za polovic. Objednávky "
                     "rostou, konverze rostou, vy tratíte. "
                     "Vím, jsou to naivní příklady a s takovou agenturou nebudete chtít dlouhodobě spolupracovat. "
                     "Ale to rozhodně nejsou všechny nástroje, které může agentura použít. "
                     "Lidé se dají oblbnout. Existují typy úprav webu, které zvyšují konverzní poměr a využívají "
                     "automatických reakcí nebo snížené pozornosti návštěvníků. Říká se jim v designerské hantýrce "
                     "dark patterns. Jejich použití není etické a z dlouhodobého hlediska je především hloupé. "
                     "Budete riskovat ztrátu dobrého jména? Na čistě finančních ukazatelích to letos nepoznáte a "
                     "pokud nechcete firmu rychle prodat, tak to nedává smysl. "
                     "I když bude agentura chtít dělat svou práci dobře, tak bude mít každý zásah do webu nezamýšlené "
                     "důsledky. A ty budete buď vyhodnocovat a řešit, nebo nikoliv. A agentura závislá na změně "
                     "Dejte agentuře do smlouvy, že jí zaplatíte jen když se váš konverzní poměr zvedne o X, a agentura"
                     "se nebude soustředit na nic jiného, než na váš konverzní poměr. V té chvíli nesedíte na stejné "
                     "straně stolu — místo partnerství vytěžujete svůj nový zdroj, tedy agenturu. "
                     "Agentura chce dostat zaplaceno a když chcete vyšší konverze, dostanete vyšší konverze. "
                     "Nejjednodušší způsob, jak zvýšit konverze je odbourat návštěvnost, která nekonvertuje. Říkejme "
                     "tomu třeba optimalizace kvality návštěvnosti. Něco zakážete v robots.txt, něco smažete a "
                     "konverze jsou najednou 2%. Kliente plať. "
                     "Druhá nejjednodušší možnost je sleva. Masivní slevová kampaň, všechno za polovic. Objednávky "
                     "rostou, konverze rostou, vy tratíte. "
                     "Vím, jsou to naivní příklady a s takovou agenturou nebudete chtít dlouhodobě spolupracovat. "
                     "Ale to rozhodně nejsou všechny nástroje, které může agentura použít. "
                     "Lidé se dají oblbnout. Existují typy úprav webu, které zvyšují konverzní poměr a využívají "
                     "automatických reakcí nebo snížené pozornosti návštěvníků. Říká se jim v designerské hantýrce "
                     "dark patterns. Jejich použití není etické a z dlouhodobého hlediska je především hloupé. "
                     "Budete riskovat ztrátu dobrého jména? Na čistě finančních ukazatelích to letos nepoznáte a "
                     "pokud nechcete firmu rychle prodat, tak to nedává smysl. "
                     "I když bude agentura chtít dělat svou práci dobře, tak bude mít každý zásah do webu nezamýšlené "
                     "důsledky. A ty budete buď vyhodnocovat a řešit, nebo nikoliv. A agentura závislá na změně "
                     "jedné metriky je řešit nebude.",
            'bank_transfer': True,
            'post_office_cash': True,
            'pay_frequency': 2,
            'users': [{'id': u2.id}],
        },
            context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('notes', serializer.errors.keys())

    def test_validate_without_payment_type(self):
        c = baker.make('companies.Company', commission=5)
        user = baker.make('users.User', role=user_constants.USER_ROLE_ADMIN, company=c)
        u2 = baker.make('users.User', role=user_constants.USER_ROLE_CRA, company=c)
        request = Request()
        request.user = user

        serializer = serializers.StudyWriteSerializer(data={
            'number': 1,
            'identifier': 'test',
            'notes': 'test',
            'bank_transfer': False,
            'post_office_cash': False,
            'pay_frequency': 2,
            'users': [{'id': u2.id}],
            'bank_account': '7998862/0800',
        },
            context={'request': request})
        self.assertFalse(serializer.is_valid())
        self.assertIn('bank_transfer', serializer.errors.keys())
        self.assertIn('post_office_cash', serializer.errors.keys())

    def test_validate_status_billing_with_reims_not_approved(self):
        study = baker.make('studies.Study', status=constants.STUDY_STATUS_PROGRESS)
        pvi = baker.make('studies.PatientVisitItem', patient_visit__study=study, approved=None)
        data = {
            'status': constants.STUDY_STATUS_BILLING,
        }
        serializer = serializers.StudyWriteSerializer(study, data=data, partial=True)
        self.assertFalse(serializer.is_valid())
        self.assertIn('status', serializer.errors.keys())

    def test_validate_status_billing_with_reims_approved(self):
        study = baker.make('studies.Study', status=constants.STUDY_STATUS_PROGRESS)
        pvi = baker.make('studies.PatientVisitItem', patient_visit__study=study, approved=True)
        data = {
            'status': constants.STUDY_STATUS_BILLING,
        }
        serializer = serializers.StudyWriteSerializer(study, data=data, partial=True)
        self.assertTrue(serializer.is_valid())
