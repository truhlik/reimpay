from django_filters.rest_framework import DjangoFilterBackend


class CustomDjangoFilterBackend(DjangoFilterBackend):

    def get_coreschema_field(self, field):
        field_cls = super(CustomDjangoFilterBackend, self).get_coreschema_field(field)
        if field_cls.description == None or field_cls.description == '':
            field_cls.description = 'Dummy help text'
        return field_cls
