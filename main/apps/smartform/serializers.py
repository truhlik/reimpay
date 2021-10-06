from rest_framework import serializers


class AddressSuggestionSerializer(serializers.Serializer):
    city = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    street = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    number = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    post_code = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    suggesting_field = serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def validate(self, attrs):
        data_list = []
        data_list.append(attrs.get('city', '') != '')
        data_list.append(attrs.get('street', '') != '')
        data_list.append(attrs.get('number', '') != '')
        data_list.append(attrs.get('post_code', '') != '')

        # pokud mám alespoň jeden field vyplněný, tak je to OK
        if not any(data_list):
            raise serializers.ValidationError('You must send at least one field [street, city, post_code]')
        return attrs


class AddressResponseSerializer(serializers.Serializer):
    results = AddressSuggestionSerializer(many=True)
