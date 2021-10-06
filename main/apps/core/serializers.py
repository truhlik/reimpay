from rest_framework import serializers

from main.apps.studies.models import Study, Patient
from main.apps.studies.utils import create_stats


class CreditInfoSerializer(serializers.ModelSerializer):
    actual_balance = serializers.CharField()
    paid = serializers.CharField()
    max_cost = serializers.CharField()
    remaining_visits = serializers.IntegerField()
    avg_visit_value = serializers.CharField()
    exp_budget_need = serializers.CharField()

    class Meta:
        model = Study
        fields = [
            'actual_balance', 'paid', 'max_cost', 'remaining_visits', 'avg_visit_value', 'exp_budget_need'
        ]


class StudyStatSerializer(serializers.ModelSerializer):
    stats = serializers.SerializerMethodField()

    class Meta:
        model = Study
        fields = ['stats']

    def get_stats(self, obj):
        return create_stats(obj)


class DoctorLoginSerializer(serializers.Serializer):
    patient_number = serializers.CharField(required=True)
    site_pin = serializers.CharField(required=True)

    def validate(self, attrs):
        patient_number = attrs.get('patient_number', None)
        site_pin = attrs.get('site_pin', None)
        patient = Patient.objects.filter(site__pin=site_pin, number=patient_number).first()
        if patient_number is None or site_pin is None or patient is None:
            raise serializers.ValidationError('You must enter valid combination of patient number and site pin.')
        attrs['patient'] = patient
        return attrs
