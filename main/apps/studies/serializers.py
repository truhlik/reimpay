import urllib

from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext as _

from rest_framework import serializers

from main.apps.studies.logic import StudyStatusValidation
from main.apps.users.models import User
from main.apps.users.serializers import UserSerializer
from . import models, constants, utils
from ..core.constants import PAYMENT_TYPE_BANK_TRANSFER, PAYMENT_TYPE_POST_OFFICE
from main.libraries.functions import get_absolute_url
from main.libraries.permissions import is_doctor, check_patient_id_in_session
from main.libraries.utils import validate_bank_number


class PermissionMixin(object):

    def _get_study_object(self, attrs):
        raise NotImplementedError()

    def validate(self, attrs):
        # zvaliduju vytvoření objektu
        if self.instance is None and not utils.can_be_created(self.Meta.model, self._get_study_object(attrs)):
            raise serializers.ValidationError(
                "{} can't be created if study in in {} status.".format(self.get_object_name(),
                                                                       self._get_study_object(attrs).get_status_display()))
        return attrs

    def get_object_name(self):
        return self.Meta.model._meta.model_name


class BaseStudySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    # denormalized fields
    active_patients = serializers.SerializerMethodField()
    paid = serializers.SerializerMethodField()
    credit = serializers.SerializerMethodField()
    date_launched = serializers.DateTimeField(read_only=True, source='progress_at', format="%Y-%m-%d")
    date_last_visit = serializers.DateField(read_only=True)
    pay_frequency = serializers.IntegerField(min_value=0)
    bank_account = serializers.CharField(required=True)

    class Meta:
        model = models.Study
        fields = [
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
        ]

    def get_active_patients(self, obj):
        return len(obj.patients.all())

    def get_paid(self, obj):
        from main.apps.core.utils import get_paid
        return abs(get_paid(obj) / settings.INT_RATIO)

    def get_credit(self, obj):
        from main.apps.core.utils import get_actual_balance
        return get_actual_balance(obj) / settings.INT_RATIO

    def validate_bank_account(self, bank_account):
        if bank_account is None or bank_account == '':
            return bank_account

        if not validate_bank_number(bank_account):
            raise serializers.ValidationError("This account number is not valid.")
        return bank_account


class StudyReadSerializer(BaseStudySerializer):
    status = serializers.ChoiceField(choices=constants.STUDY_STATUS_CHOICES, read_only=True)


class UserInnerSerializer(serializers.PrimaryKeyRelatedField):

    def to_representation(self, value):
        data = super(UserInnerSerializer, self).to_representation(value)
        return {'id': data}

    def to_internal_value(self, data):
        data = data['id']
        return super(UserInnerSerializer, self).to_internal_value(data)


class StudyWriteSerializer(BaseStudySerializer):

    def validate(self, attrs):
        post_office_cash = attrs.get('post_office_cash', None)
        bank_transfer = attrs.get('bank_transfer', None)

        # pokud alespoň jeden není True, tak vrať error
        if post_office_cash is False and bank_transfer is False or \
                self.instance is None and post_office_cash is None and bank_transfer is None:
            raise serializers.ValidationError({
                'post_office_cash': "You must choose at least one payment method",
                'bank_transfer': "You must choose at least one payment method",
            })
        return attrs

    def validate_status(self, status):
        if status is None:
            return status
        if not StudyStatusValidation(self.instance).can_change_status(status):
            raise serializers.ValidationError("This change of status is not allowed.")
        return status

    def create(self, validated_data):
        validated_data['company'] = self.context['request'].user.company
        validated_data['commission'] = self.context['request'].user.company.commission
        validated_data['variable_symbol'] = utils.generate_variable_symbol()
        instance = super(StudyWriteSerializer, self).create(validated_data)
        utils.create_base_visit_map(instance)
        return instance


class StudyConfigSerializer(serializers.ModelSerializer):
    config = serializers.SerializerMethodField()

    class Meta:
        model = models.Study
        fields = [
            'config',
        ]

    def get_config(self, obj):
        return utils.get_config(obj)


class StudyRelatedSerializerMixin(object):

    def validate_study(self, study: models.Study):
        if study is None:
            return study

        if not study.is_owner(self.context['request'].user):
            raise serializers.ValidationError(_("you are not owner of given study"))
        return study


class StudyItemSerializer(PermissionMixin, StudyRelatedSerializerMixin, serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    study = serializers.PrimaryKeyRelatedField(queryset=models.Study.objects.all(), required=True)
    price = serializers.IntegerField(min_value=0)

    class Meta:
        model = models.StudyItem
        fields = [
            'id',
            'title',
            'description',
            'price',
            'study',
        ]

    def _get_study_object(self, attrs):
        return attrs.get('study', None)

    def validate(self, attrs):
        return super(StudyItemSerializer, self).validate(attrs)


class ArmSerializer(PermissionMixin, StudyRelatedSerializerMixin, serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    max_unscheduled = serializers.IntegerField(min_value=0, required=False)

    class Meta:
        model = models.Arm
        fields = [
            'id',
            'title',
            'study',
            'max_unscheduled',
        ]

    def create(self, validated_data):
        instance = super(ArmSerializer, self).create(validated_data)
        utils.create_visits(instance.study, instance)
        return instance

    def _get_study_object(self, attrs):
        return attrs.get('study', None)

    def validate(self, attrs):
        return super(ArmSerializer, self).validate(attrs)


class SiteSerializer(PermissionMixin, StudyRelatedSerializerMixin, serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    cra = serializers.PrimaryKeyRelatedField(queryset=User.objects.active().cra(), required=True, write_only=True)
    cra_obj = UserSerializer(read_only=True, source='cra')
    expected_patients = serializers.IntegerField(min_value=0, required=False)
    contract_path = serializers.SerializerMethodField()
    site_instructions_path = serializers.SerializerMethodField()

    class Meta:
        model = models.Site
        fields = [
            'id',
            'title',
            'study',
            'expected_patients',
            'cra',
            'cra_obj',
            'contract_path',
            'site_instructions_path',
        ]

    def validate_cra(self, cra_user):
        if cra_user is None:
            return cra_user

        if cra_user.company != self.context['request'].user.company:
            raise serializers.ValidationError('Given CRA is not from the same company.')
        return cra_user

    def get_contract_path(self, obj):
        return get_absolute_url(urllib.parse.unquote(reverse('sites-patient-form-pdf', args=(obj.id, ))))

    def get_site_instructions_path(self, obj):
        return get_absolute_url(urllib.parse.unquote(reverse('sites-instruction-pdf', args=(obj.id, ))))

    def _get_study_object(self, attrs):
        return attrs.get('study', None)

    def create(self, validated_data):
        validated_data['pin'] = utils.generate_site_pin()
        return super(SiteSerializer, self).create(validated_data)


class BooleanToDatetime(serializers.BooleanField):

    def to_internal_value(self, data):
        if data is True:
            return timezone.now()
        else:
            return None

    def to_representation(self, value):
        return bool(value)


class BlankEditCharField(serializers.CharField):

    def to_representation(self, value):
        return ""


class PatientBaseSerializer(PermissionMixin, StudyRelatedSerializerMixin, serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    number = serializers.CharField(required=True, min_length=4)
    arm_name = serializers.CharField(read_only=True, source='arm.title')
    visits = serializers.IntegerField(read_only=True, source='visits_count')
    paid = serializers.IntegerField(default=0, read_only=True)
    site_obj = SiteSerializer(read_only=True, source='site')
    change_payment_request = BooleanToDatetime(required=False)
    status = serializers.CharField(read_only=True)

    payment_info = BlankEditCharField(required=False, allow_blank=True, allow_null=True)
    name = BlankEditCharField(required=False, allow_blank=True, allow_null=True)
    street = BlankEditCharField(required=False, allow_blank=True, allow_null=True)
    street_number = BlankEditCharField(required=False, allow_blank=True, allow_null=True)
    city = BlankEditCharField(required=False, allow_blank=True, allow_null=True)
    zip = BlankEditCharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = models.Patient
        fields = [
            'id', 'arm', 'number', 'payment_type', 'payment_info', 'arm_name', 'visits', 'paid', 'site',
            'name', 'street', 'street_number', 'city', 'zip', 'site_obj', 'change_payment_request', 'status',
        ]

    def validate_arm(self, arm):
        if arm is None:
            return arm

        if not arm.is_owner(self.context['request'].user):
            raise serializers.ValidationError('This arm cannot be used for this Patient.')

        if self.instance is not None and self.instance.arm != arm:
            raise serializers.ValidationError('You cant change arm for already create Patient.')
        return arm

    def validate_number(self, number):
        if number is None:
            return number

        if self.instance is not None and self.instance.number != number:
            raise serializers.ValidationError("You can't change number for already created Patient.")
        return number

    def validate_site(self, site):
        if site is None:
            return site

        if not site.is_owner(self.context['request'].user):
            raise serializers.ValidationError('This site cannot be used for this Patient.')
        return site

    def validate_payment_info(self, payment_info):
        if payment_info is None or payment_info == "":
            return payment_info

        if not validate_bank_number(payment_info):
            raise serializers.ValidationError("This account number is not valid.")
        return payment_info

    def validate(self, attrs):
        attrs = super(PatientBaseSerializer, self).validate(attrs)
        arm = attrs.get('arm', None)
        site = attrs.get('site', None)
        number = attrs.get('number', None)
        payment_type = attrs.get('payment_type', None)
        payment_info = attrs.get('payment_info', None)

        name = attrs.get('name', None)
        street = attrs.get('street', None)
        street_number = attrs.get('street_number', None)
        city = attrs.get('city', None)
        zip = attrs.get('zip', None)

        if arm and site and arm.study_id != site.study_id:
            raise serializers.ValidationError({'arm': 'This arm does not match with given site.'})

        if site and payment_type and not site.study.is_payment_method_allowed(payment_type):
            raise serializers.ValidationError({'payment_type': 'This payment_type is not allowed for this study.'})

        if payment_type == PAYMENT_TYPE_BANK_TRANSFER and not payment_info:
            raise serializers.ValidationError({'payment_info': 'You must provide payment_info.'})

        address_info = all([name, street, street_number, city, zip])
        if payment_type == PAYMENT_TYPE_POST_OFFICE and not address_info:
            if not name:
                raise serializers.ValidationError({'name': 'You must provide name address information.'})
            if not street:
                raise serializers.ValidationError({'street': 'You must provide street address information.'})
            if not street_number:
                raise serializers.ValidationError({'street_number': 'You must provide street_number address information.'})
            if not city:
                raise serializers.ValidationError({'city': 'You must provide city address information.'})
            if not zip:
                raise serializers.ValidationError({'zip': 'You must provide zip address information.'})

        if number and site:
            qs = models.Patient.objects.filter(study=site.study, number=number)
            if self.instance:  # musím excludnout sebe
                qs = qs.exclude(id=self.instance.id)
            if qs.exists():
                raise serializers.ValidationError({'number': 'This number is already given to another patient in this study.'})

        # pokud chci změnit jakýkoliv platební údaj, tak musím mít number (jako validaci)
        if self.instance and number is None and any([name, street, street_number, city, zip]):
            raise serializers.ValidationError({'number': 'You must provide number for any change on patient.'})

        return attrs

    def _get_study_object(self, attrs):
        site = attrs.get('site', None)
        return site.study if site is not None else None


class SitePatientSerializer(serializers.ModelSerializer):
    patients = PatientBaseSerializer(many=True)
    contract_path = serializers.SerializerMethodField()
    site_instructions_path = serializers.SerializerMethodField()

    class Meta:
        model = models.Site
        fields = [
            'patients',
            'id',
            'title',
            'study',
            'expected_patients',
            'cra',
            'contract_path',
            'site_instructions_path',
        ]

    def get_contract_path(self, obj):
        return get_absolute_url(urllib.parse.unquote(reverse('sites-patient-form-pdf', args=(obj.id, ))))

    def get_site_instructions_path(self, obj):
        return get_absolute_url(urllib.parse.unquote(reverse('sites-instruction-pdf', args=(obj.id, ))))


class BaseVisitSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True, source='__str__')
    visit_type = serializers.CharField(read_only=True)
    number = serializers.IntegerField(required=False, allow_null=True, min_value=0)

    class Meta:
        model = models.Visit
        fields = [
            'id',
            'arm',
            'name',
            'title',
            'number',
            'visit_type',
            'order',
        ]

    def validate_order(self, order):
        if order is None:
            return order
        if order <= 0:
            raise serializers.ValidationError('order must be greater then zero')
        if order >= constants.STUDY_VISIT_UNSCHEDULED_ORDER:
            raise serializers.ValidationError('you must use lower order number')
        return order

    def validate(self, args):
        arm = args.get('arm', None)
        visit_items = args.get('visit_items', None)

        # zkontroluju, že sedí arm a study item
        if visit_items and arm:
            study_id = arm.study_id
            for item in visit_items['active']:
                if item['study_item'].study_id != study_id:
                    raise serializers.ValidationError({'visit_items': _('study item does not belong to same study')})
        return args

    def validate_arm(self, arm):
        if arm is None:
            return arm

        if not arm.is_owner(self.context['request'].user):
            raise serializers.ValidationError({'arm': 'This arm cannot be used for this Visit.'})
        return arm


class VisitItemSerializer(PermissionMixin, serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    study_item_obj = StudyItemSerializer(read_only=True, source='study_item')
    study_item = serializers.PrimaryKeyRelatedField(queryset=models.StudyItem.objects.active())
    visit = serializers.PrimaryKeyRelatedField(required=False, queryset=models.Visit.objects.active())
    visit_obj = BaseVisitSerializer(read_only=True, source='visit')

    class Meta:
        model = models.VisitItem
        fields = [
            'id',
            'visit',
            'study_item',
            'study_item_obj',
            'visit_obj',
        ]

    def validate_study_item(self, study_item):
        if study_item is None:
            return study_item

        if not study_item.is_owner(self.context['request'].user):
            raise serializers.ValidationError({'study_item': 'This study item cannot be used for this visit item.'})
        return study_item

    def validate_visit(self, visit):
        if visit is None:
            return visit

        if not visit.is_owner(self.context['request'].user):
            raise serializers.ValidationError({'visit': 'This visit cannot be used for this visit item.'})
        return visit

    def validate(self, attrs):
        attrs = super(VisitItemSerializer, self).validate(attrs)
        visit = attrs.get('visit', None)
        study_item = attrs.get('study_item', None)

        if study_item and visit and study_item.study_id != visit.study_id:
            raise serializers.ValidationError({'visit': 'This visit does not belong match the study item.'})
        return attrs

    def _get_study_object(self, attrs):
        study_item = attrs.get('study_item', None)
        return study_item.study if study_item is not None else None


class VisitSerializer(PermissionMixin, BaseVisitSerializer):
    visit_items = VisitItemSerializer(many=True, source='visit_items.active', required=False)
    visit_items_cost = serializers.IntegerField(read_only=True, source='arm.d_visit_items_cost')

    class Meta:
        model = models.Visit
        fields = [
            'id',
            'arm',
            'name',
            'title',
            'number',
            'visit_type',
            'visit_items',
            'order',
            'visit_items_cost',
        ]

    def validate_visit_items(self, visit_items):
        if not visit_items:
            return visit_items

        if self.instance and visit_items:
            raise serializers.ValidationError('cannot update visit with visit items in data')
        return visit_items

    def create(self, validated_data):
        # automaticky vytvoř název visity, pokud není definován
        title = validated_data.get('title', None)
        order = validated_data.get('order', None)
        if title is None:
            validated_data['title'] = "{}. visit".format(order or "?")

        # z frontu lze vytvářet pouze REGULAR VISITS
        validated_data['visit_type'] = constants.STUDY_VISIT_TYPE_REGULAR

        # abych umožnil kopírování včetně visit items, tak tu mám tenhle kód
        visit_items = validated_data.pop('visit_items', {})
        visit = super(VisitSerializer, self).create(validated_data)
        for item in visit_items.get('active', []):
            models.VisitItem.objects.create(visit=visit, **item)
        return visit

    def update(self, instance, validated_data):
        visit_items = validated_data.pop('visit_items', {})
        if visit_items:
            raise NotImplementedError('update with visit items is not supported')
        return super(VisitSerializer, self).update(instance, validated_data)

    def _get_study_object(self, attrs):
        arm = attrs.get('arm', None)
        return arm.study if arm is not None else None

    def validate(self, attrs):
        return super(VisitSerializer, self).validate(attrs)


class PatientVisitSerializer(PermissionMixin, serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    visit_type = serializers.ChoiceField(choices=constants.STUDY_VISIT_TYPE_CHOICES, write_only=True)
    visit_items = serializers.PrimaryKeyRelatedField(queryset=models.VisitItem.objects.active(), many=True, required=False)
    visit = serializers.PrimaryKeyRelatedField(read_only=True)
    title = serializers.SerializerMethodField()

    class Meta:
        model = models.PatientVisit
        fields = [
            'id',
            'patient',
            'visit_type',
            'visit_date',
            'visit_items',
            'visit',
            'title',
        ]

    def get_title(self, obj):
        return "{} {}".format(obj.visit.title or str(obj), str(obj.visit_date))

    def _get_study_object(self, attrs):
        patient = attrs.get('patient', None)
        return patient.study if patient is not None else None

    def validate(self, attrs):
        super(PatientVisitSerializer, self).validate(attrs)
        patient = attrs.get('patient', None)
        visit_type = attrs.get('visit_type', None)
        visit_items = attrs.get('visit_items', None)

        if not utils.can_change_visit_type_for_patient_visit(self.instance, patient, visit_type):
            raise serializers.ValidationError('This visit type cannot be chosen.')

        if visit_items and patient:
            # zjistím, zda všechny visit_items jsou available pro tohoto pacienta
            available_items = utils.filter_available_visit_items(models.VisitItem.objects.active(),
                                                                 patient.id,
                                                                 visit_type,
                                                                 next_only=True)
            for item in visit_items:
                if item not in available_items:
                    raise serializers.ValidationError({'visit_items': _('Visit item is not available.')})

        return attrs

    def validate_patient(self, patient):
        if patient is None:
            return patient

        user = self.context['request'].user

        # pozor Doktor nemusí být authenticated, takže proto je tu ta podmínka jen pro auth usery
        if user.is_authenticated and not patient.is_owner(user):
            raise serializers.ValidationError('You dont have permission to manage visits for this patient.')

        if is_doctor(self.context['request']) and not check_patient_id_in_session(self.context['request'], patient.id):
            raise serializers.ValidationError('You dont have permission to manage visits for this patient.')
        return patient

    def validate_visit_date(self, visit_date):
        if visit_date is None:
            return visit_date
        if visit_date > timezone.now().date():
            raise serializers.ValidationError('You cant make visit in the future.')
        return visit_date

    def validate_visit_items(self, visit_items):
        if not visit_items:
            return visit_items

        visit_id = None
        for item in visit_items:
            visit_id = item.visit_id if visit_id is None else visit_id  # uložím si do visit_id první ID Visit
            if visit_id != item.visit_id:
                raise serializers.ValidationError(_('You cant choose visit items from multiple visits'))
        return visit_items

    def _get_visit(self, patient, visit_type: str):
        visits = utils.get_patient_available_visits(patient)
        for v in visits:
            if v.visit_type == visit_type:
                return v
        return None

    def save(self, **kwargs):
        visit_type = self.validated_data.pop('visit_type')
        items = self.validated_data.get('visit_items')
        patient = self.validated_data['patient']

        # musím tam vrazit visit, protože visit items je m2m a tak se savuje až po visitě
        self.validated_data['visit'] = self._get_visit(patient, visit_type)
        instance = super(PatientVisitSerializer, self).save(**kwargs)

        # musím nastavit původ Reimsů
        if items:
            instance.patient_visit_items.filter(visit_item__in=items)\
                .update(origin=constants.STUDY_PATIENT_VISIT_ITEM_ORIGIN_SITE)

        return instance


class PatientVisitItemSerializer(PermissionMixin, serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    visit_item = serializers.PrimaryKeyRelatedField(write_only=True, queryset=models.VisitItem.objects.active())
    patient_visit = serializers.PrimaryKeyRelatedField(queryset=models.PatientVisit.objects.all())

    visit_item_obj = VisitItemSerializer(read_only=True, source='visit_item')
    patient_obj = PatientBaseSerializer(read_only=True, source='patient_visit.patient')
    date = serializers.DateField(source='patient_visit.visit_date', read_only=True)
    approved = serializers.NullBooleanField(required=False)
    status = serializers.CharField(read_only=True)
    origin = serializers.CharField(read_only=True)
    reject_reason = serializers.CharField(required=False)
    flagged = serializers.SerializerMethodField()
    can_be_deleted = serializers.SerializerMethodField()

    class Meta:
        model = models.PatientVisitItem
        fields = [
            'id',
            'visit_item',
            'patient_visit',
            'visit_item_obj',
            'patient_obj',
            'date',
            'approved',
            'status',
            'origin',
            'reject_reason',
            'flagged',
            'can_be_deleted',
        ]

    def get_can_be_deleted(self, obj):
        return utils.can_delete_patient_visit(obj.patient_visit)

    def get_flagged(self, obj):
        patient = obj.patient_visit.patient
        return obj.approved is None and patient.change_payment_request

    def validate_approved(self, approved):
        # zamezím změně approved po té co je již jednou nastavena
        if self.instance and self.instance.approved is not None and approved != self.instance.approved:
            raise serializers.ValidationError('you cant change approved yet')
        return approved

    def validate_patient_visit(self, patient_visit):
        if patient_visit is None:
            return patient_visit
        if not patient_visit.patient.is_owner(self.context['request'].user):
            raise serializers.ValidationError('you cant manage this patient visit')
        return patient_visit

    def validate_visit_item(self, visit_item):
        if visit_item is None:
            return visit_item
        # todo budou potřeba nějaké validace na visit item nebo ne?
        return visit_item

    def _get_study_object(self, attrs):
        visit_item = attrs.get('visit_item', None)
        return visit_item.study if visit_item else None

    def validate(self, attrs):
        super(PatientVisitItemSerializer, self).validate(attrs)
        visit_item = attrs.get('visit_item', None)
        patient_visit = attrs.get('patient_visit', None)

        if patient_visit and visit_item and visit_item.visit != patient_visit.visit:
            raise serializers.ValidationError({'visit_item': "you can't choose this visit item, does not match for patient visit"})

        self._validate_credit_balance(attrs)

        return attrs

    def _validate_credit_balance(self, attrs):
        from main.apps.core.utils import get_actual_balance
        approved = attrs.get('approved', None)
        visit_item = attrs.get('visit_item', self.instance.visit_item if self.instance else None)

        if not approved:
            return

        if not visit_item:
            raise serializers.ValidationError({'visit_item': 'unable to validate credit balance'})

        study = visit_item.study

        actual_credit = get_actual_balance(study)
        expense = visit_item.study_item.price * settings.INT_RATIO + \
                  (visit_item.study_item.price * settings.INT_RATIO * study.commission / 100) + \
                  utils.get_payment_method_fee(PAYMENT_TYPE_POST_OFFICE, 10000)
        if actual_credit < expense:
            raise serializers.ValidationError({"You don't have enough credit for this study."})
        return

    def save(self, **kwargs):
        instance = super(PatientVisitItemSerializer, self).save(**kwargs)
        return instance

    def create(self, validated_data):
        validated_data['origin'] = constants.STUDY_PATIENT_VISIT_ITEM_ORIGIN_CRA
        return super(PatientVisitItemSerializer, self).create(validated_data)


class PatientVisitItemNormalizedSerializer(serializers.ModelSerializer):
    payment = serializers.IntegerField(source='id', read_only=True)
    visit = serializers.CharField(source='visit_item.visit.title', read_only=True)
    date = serializers.DateField(source='patient_visit.visit_date', read_only=True)
    amount = serializers.IntegerField(source='visit_item.study_item.price', read_only=True)
    note = serializers.CharField(default='Poznámka', read_only=True)

    class Meta:
        model = models.PatientVisitItem
        fields = [
            'payment',
            'visit',
            'date',
            'amount',
            'note',
            'payment_status',
            'reject_reason',
        ]


class PatientDetailSerializer(PatientBaseSerializer):
    next_visits = VisitSerializer(read_only=True, many=True)
    study_obj = BaseStudySerializer(read_only=True, source='study')
    patient_visit_items = PatientVisitItemNormalizedSerializer(read_only=True, many=True)
    unscheduled_left = serializers.SerializerMethodField()

    class Meta:
        model = models.Patient
        fields = [
            'id',
            'arm',
            'number',
            'payment_type',
            'payment_info',
            'arm_name',
            'visits',
            'paid',
            'site',
            'next_visits',
            'study_obj',
            'patient_visit_items',
            'unscheduled_left'
        ]

    def get_unscheduled_left(self, obj):
        return max(obj.arm.max_unscheduled - utils.get_unscheduled_visits(obj).count(), 0)

