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
        # serializer je validn?? i kdy?? tam pos??l??m ??patn?? users, proto??e on je ignoruje
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
            'notes': "Dejte agentu??e do smlouvy, ??e j?? zaplat??te jen kdy?? se v???? konverzn?? pom??r zvedne o X, a agentura"
                     "se nebude soust??edit na nic jin??ho, ne?? na v???? konverzn?? pom??r. V t?? chv??li nesed??te na stejn?? "
                     "stran?? stolu ??? m??sto partnerstv?? vyt????ujete sv??j nov?? zdroj, tedy agenturu. "
                     "Agentura chce dostat zaplaceno a kdy?? chcete vy?????? konverze, dostanete vy?????? konverze. "
                     "Nejjednodu?????? zp??sob, jak zv????it konverze je odbourat n??v??t??vnost, kter?? nekonvertuje. ????kejme "
                     "tomu t??eba optimalizace kvality n??v??t??vnosti. N??co zak????ete v robots.txt, n??co sma??ete a "
                     "konverze jsou najednou 2%. Kliente pla??. "
                     "Druh?? nejjednodu?????? mo??nost je sleva. Masivn?? slevov?? kampa??, v??echno za polovic. Objedn??vky "
                     "rostou, konverze rostou, vy trat??te. "
                     "V??m, jsou to naivn?? p????klady a s takovou agenturou nebudete cht??t dlouhodob?? spolupracovat. "
                     "Ale to rozhodn?? nejsou v??echny n??stroje, kter?? m????e agentura pou????t. "
                     "Lid?? se daj?? oblbnout. Existuj?? typy ??prav webu, kter?? zvy??uj?? konverzn?? pom??r a vyu????vaj?? "
                     "automatick??ch reakc?? nebo sn????en?? pozornosti n??v??t??vn??k??. ????k?? se jim v designersk?? hant??rce "
                     "dark patterns. Jejich pou??it?? nen?? etick?? a z dlouhodob??ho hlediska je p??edev????m hloup??. "
                     "Budete riskovat ztr??tu dobr??ho jm??na? Na ??ist?? finan??n??ch ukazatel??ch to letos nepozn??te a "
                     "pokud nechcete firmu rychle prodat, tak to ned??v?? smysl. "
                     "I kdy?? bude agentura cht??t d??lat svou pr??ci dob??e, tak bude m??t ka??d?? z??sah do webu nezam????len?? "
                     "d??sledky. A ty budete bu?? vyhodnocovat a ??e??it, nebo nikoliv. A agentura z??visl?? na zm??n?? "
                     "Dejte agentu??e do smlouvy, ??e j?? zaplat??te jen kdy?? se v???? konverzn?? pom??r zvedne o X, a agentura"
                     "se nebude soust??edit na nic jin??ho, ne?? na v???? konverzn?? pom??r. V t?? chv??li nesed??te na stejn?? "
                     "stran?? stolu ??? m??sto partnerstv?? vyt????ujete sv??j nov?? zdroj, tedy agenturu. "
                     "Agentura chce dostat zaplaceno a kdy?? chcete vy?????? konverze, dostanete vy?????? konverze. "
                     "Nejjednodu?????? zp??sob, jak zv????it konverze je odbourat n??v??t??vnost, kter?? nekonvertuje. ????kejme "
                     "tomu t??eba optimalizace kvality n??v??t??vnosti. N??co zak????ete v robots.txt, n??co sma??ete a "
                     "konverze jsou najednou 2%. Kliente pla??. "
                     "Druh?? nejjednodu?????? mo??nost je sleva. Masivn?? slevov?? kampa??, v??echno za polovic. Objedn??vky "
                     "rostou, konverze rostou, vy trat??te. "
                     "V??m, jsou to naivn?? p????klady a s takovou agenturou nebudete cht??t dlouhodob?? spolupracovat. "
                     "Ale to rozhodn?? nejsou v??echny n??stroje, kter?? m????e agentura pou????t. "
                     "Lid?? se daj?? oblbnout. Existuj?? typy ??prav webu, kter?? zvy??uj?? konverzn?? pom??r a vyu????vaj?? "
                     "automatick??ch reakc?? nebo sn????en?? pozornosti n??v??t??vn??k??. ????k?? se jim v designersk?? hant??rce "
                     "dark patterns. Jejich pou??it?? nen?? etick?? a z dlouhodob??ho hlediska je p??edev????m hloup??. "
                     "Budete riskovat ztr??tu dobr??ho jm??na? Na ??ist?? finan??n??ch ukazatel??ch to letos nepozn??te a "
                     "pokud nechcete firmu rychle prodat, tak to ned??v?? smysl. "
                     "I kdy?? bude agentura cht??t d??lat svou pr??ci dob??e, tak bude m??t ka??d?? z??sah do webu nezam????len?? "
                     "d??sledky. A ty budete bu?? vyhodnocovat a ??e??it, nebo nikoliv. A agentura z??visl?? na zm??n?? "
                     "jedn?? metriky je ??e??it nebude.",
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
