from rest_framework import serializers

from main.libraries.serializers.mixins import DynamicFieldsMixin
from .models import Company
from ...libraries.functions import get_absolute_url


class BaseCompanySerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    # todo uncomment when sorl-thumbnail==12.6.0 will be released on Pypi
    # image = HyperlinkedSorlImageField('128x128', options={"crop": "center"}, read_only=True)
    image = serializers.SerializerMethodField()
    reg_number = serializers.CharField(required=True)
    address = serializers.CharField(read_only=True)
    web = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Company
        fields = [
            'id',
            'name',
            'image',
            'description',
            'email',
            'phone',
            'web',
            'reg_number',
            'vat_number',
            'street',
            'street_number',
            'city',
            'zip',
            'address',
        ]

    def get_image(self, obj):
        if obj.image:
            return get_absolute_url(obj.image.url)
        return ''


