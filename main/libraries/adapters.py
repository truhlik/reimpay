from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from main.apps.users.models import User


class AutoSignupAdapter(DefaultSocialAccountAdapter):
    """
    Automatically connects existing account with social login if same email already exists
    There are some alternatives https://github.com/pennersr/django-allauth/issues/418
    """
    def pre_social_login(self, request, sociallogin):
        try:
            email = sociallogin.account.extra_data.get('email')
            if email:
                user = User.objects.get(email=email)
                if not sociallogin.is_existing:
                    sociallogin.connect(request, user)
        except User.DoesNotExist:
            pass


class CustomDefaultAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        user = super(CustomDefaultAccountAdapter, self).save_user(request, user, form, commit)
        # todo do some stuff with user
        return user
