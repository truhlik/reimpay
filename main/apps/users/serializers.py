import urllib

from django.conf import settings
from django.urls import reverse
from rest_auth.serializers import PasswordResetSerializer
from rest_framework import serializers

from .models import User
from .constants import USER_ROLE_CHOICES


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    email = serializers.EmailField()
    role = serializers.ChoiceField(choices=USER_ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['id', 'role', 'first_name', 'last_name', 'email']

    def validate_email(self, email):
        if email is None:
            return email
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email is already registered.')
        return email


class CustomPasswordResetSerializer(PasswordResetSerializer):

    def get_email_options(self):
        return {
            'extra_email_context': {
                'admin_url': settings.BASE_URL,
                'frontend_reset_password_url': urllib.parse.unquote(reverse('frontend_password_reset')),
            },
            'html_email_template_name': 'registration/password_reset_email.html'
        }
