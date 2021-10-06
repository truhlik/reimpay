import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager, CustomUserQuerySet
from django.utils.translation import ugettext_lazy as _
from . import constants


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(_('role'), max_length=255, choices=constants.USER_ROLE_CHOICES, blank=True, null=True)
    first_name = models.CharField(_('jméno'), max_length=64)
    last_name = models.CharField(_('příjmení'), max_length=64)
    phone = models.CharField(_('telefon'), max_length=32, blank=True, null=True)
    email = models.EmailField(_('email'), unique=True, max_length=128)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False, help_text=_('určuje možnost přístupu do administrace'))
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    company = models.ForeignKey('companies.Company', related_name='users', on_delete=models.CASCADE, blank=True, null=True)  # noqa

    objects = CustomUserManager.from_queryset(CustomUserQuerySet)()
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('uživatel')
        verbose_name_plural = _('uživatelé')
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return str(self.first_name + ' ' + self.last_name)

    def custom_delete(self):
        self.is_active = False
        self.save()

    @property
    def full_name(self):
        return str(self)

    def has_admin_role(self):
        return self.role == constants.USER_ROLE_ADMIN

    def has_cra_role(self):
        return self.role == constants.USER_ROLE_CRA

    def is_owner(self, user):
        """ Vrátí True pokud je daný user považován za vlastníka self. """
        if user.is_anonymous:
            return False
        elif user.has_admin_role():
            return self.company == user.company
        return self == user

    def can_be_edit(self):
        return True

    def can_be_deleted(self):
        return False
