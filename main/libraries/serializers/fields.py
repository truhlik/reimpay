from rest_framework import serializers
from sorl.thumbnail import get_thumbnail


class HyperlinkedSorlImageField(serializers.ImageField):

    """A Django REST Framework Field class returning hyperlinked scaled and cached images."""

    def __init__(self, geometry_string, options=dict, *args, **kwargs):
        """
        Create an instance of the HyperlinkedSorlImageField image serializer.
        Args:
            geometry_string (str): The size of your cropped image.
            options (Optional[dict]): A dict of sorl options.
            *args: (Optional) Default serializers.ImageField arguments.
            **kwargs: (Optional) Default serializers.ImageField keyword
            arguments.
        For a description of sorl geometry strings and additional sorl options,
        please see https://sorl-thumbnail.readthedocs.org/en/latest/examples.html?highlight=geometry#low-level-api-examples
        """  # NOQA
        self.geometry_string = geometry_string
        self.options = options

        super(HyperlinkedSorlImageField, self).__init__(*args, **kwargs)

    def to_representation(self, value):
        """
        Perform the actual serialization.
        Args:
            value: the image to transform
        Returns:
            a url pointing at a scaled and cached image
        """
        if not value:
            return None

        image = get_thumbnail(value, self.geometry_string, **self.options)

        try:
            request = self.context.get('request', None)
            return request.build_absolute_uri(image.url)
        except:
            try:
                return super(HyperlinkedSorlImageField, self).to_representation(image)
            except AttributeError:  # NOQA
                return super(HyperlinkedSorlImageField, self).to_native(image.url)  # NOQA

    to_native = to_representation


class DictChoiceField(serializers.Field):
    dct_choices = None

    def __init__(self, dct_choices, *args, **kwargs):
        self.dct_choices = dct_choices
        super(DictChoiceField, self).__init__(*args, **kwargs)

    def to_representation(self, value):
        return self.dct_choices.get(value, None)

    def to_internal_value(self, data):
        for k, v in self.dct_choices.items():
            if v == data:
                return k
        return None


class ChoicesSerializer(serializers.Serializer):
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_id(self, obj):
        return obj[0]

    def get_name(self, obj):
        return obj[1]
