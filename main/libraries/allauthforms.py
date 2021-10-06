import allauth
from django import forms
from django.utils.translation import ugettext_lazy as _


class SignupForm(allauth.account.forms.SignupForm):
    agreed_terms = forms.BooleanField(label=_('Souhlasím s obchodními podmínkami'))
    agreed_privacy = forms.BooleanField(label=_('Souhlasím s ochranou soukromí'))
