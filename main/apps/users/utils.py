from django.conf import settings
from django.contrib.auth.forms import PasswordResetForm

from main.apps.users.serializers import CustomPasswordResetSerializer


def send_password_reset(request, email):

    # Set some values to trigger the send_email method.
    opts = {
        'use_https': request.is_secure(),
        'from_email': settings.DEFAULT_FROM_EMAIL,
        'request': request,
        'subject_template_name': 'registration/create_user_subject.txt',
        'email_template_name': 'registration/create_user_email.html',
        'html_email_template_name': 'registration/create_user_email_html.html',
    }
    opts.update(CustomPasswordResetSerializer().get_email_options())

    form = PasswordResetForm(data={"email": email})
    form.is_valid()
    form.save(**opts)
