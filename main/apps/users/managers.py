import logging
from allauth.account.models import EmailAddress
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from django.db import models

from . import constants


logger = logging.getLogger(__name__)


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(u'Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            is_active=True,
            last_login=timezone.now(),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        EmailAddress(user=user, email=user.email, verified=True, primary=True).save()
        return user


class CustomUserQuerySet(models.QuerySet):

    def owner(self, user):
        """ Vrátí users, kterých je vlastníkem daný user = sám sebe. """
        if user.has_admin_role():
            return self.filter(company=user.company)
        elif user.has_cra_role():
            return self.filter(id=user.id)
        else:
            logger.warning('unknown role')
            return self.none()

    def active(self, active=True):
        """
        Filter users based on their is_active status.
        :param active: Can filter active, non active, all
        :return: CustomUser QuerySet
        """
        if active is not None:
            return self.filter(is_active=active)
        else:
            return self.all()

    def not_active(self):
        """
        Filter users which are not active.
        :return: CustomUser QuerySet
        """
        return self.filter(is_active=False)

    def cra(self):
        return self.filter(role=constants.USER_ROLE_CRA)

    def admins(self):
        return self.filter(role=constants.USER_ROLE_ADMIN)

    def company(self, user):
        return self.filter(company=user.company)
