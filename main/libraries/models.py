from enum import Enum
import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import CustomObjectQueryset


class BaseModel(models.Model):

    created_at = models.DateTimeField(_('Vytvořeno'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Upraveno'), auto_now=True)

    class Meta:
        abstract = True


class SimpleModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(_('Vytvořeno'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Upraveno'), auto_now=True)

    class Meta:
        abstract = True


class PublicIdModel(models.Model):
    """
    Base model using extra human-readable pseudo id field when UUID is used but some ID should be displayed
    If adding after model was created, you have to create it with null=True, RunPython and alter to null=False
    (can be done in one manual migration if done in this order), example of RunPython function filling the field:

    def fill_public_id(apps, schema_editor):
    User = apps.get_model("users", "User")

    user_queryset = User.objects.all()

    for iteration_index, user in enumerate(user_queryset):
        user.public_id = iteration_index + 1
        user.save()
    """
    public_id = models.PositiveIntegerField(null=False)  # TODO unique=True not working with PostgreSQL https://stackoverflow.com/a/11093322/7113416

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        We have to handle autoincrement manually
        """

        if self.public_id is None:
            # Get the maximum display_id value from the database
            last_public_id = type(self).objects.all().order_by('-public_id').values_list('public_id').first()[
                0]  # [0] to get value from tuple

            if last_public_id is not None:
                self.public_id = last_public_id + 1
            else:
                self.public_id = 1

        return super().save(*args, **kwargs)


class PublicIdSimpleModel(PublicIdModel, SimpleModel):

    class Meta:
        abstract = True


class CustomModel(SimpleModel):
    trash = models.BooleanField(_('Koš'), default=False)

    objects = CustomObjectQueryset.as_manager()

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super(CustomModel, self).__init__(*args, **kwargs)
        self._trash = self.trash

    def was_deleted(self):
        """
        Return if this object has been moved to trash.
        :return: bool
        """
        return self._trash is False and self.trash is True

    def was_restored(self):
        """
        Return if this object has been restored from trash.
        :return: bool
        """
        return self._trash is True and self.trash is False


class NotificationDevice(Enum):
    system = 1
    email = 2
    sms = 3


# class SMS(CustomModel):
#     """
#     Model used to store information about sent SMS messages.
#     """
#     email_to = models.CharField(_('Adresát'), max_length=128)  # CHECK nebylo by lepsi pouzit EmailField
#     text_content = models.TextField(_('Textový obsah'))
#
#     class Meta:
#         verbose_name = _(u'SMS zpráva')
#         verbose_name_plural = _(u'SMS zprávy')
#
#
# class Email(CustomModel):
#     """
#     Model used to store information about sent emails.
#     """
#     subject = models.CharField(_('Předmět'), max_length=255)
#     email_from = models.CharField(_('Odesílatel'), max_length=128)  # CHECK nebylo by lepsi pouzit EmailField
#     email_to = models.CharField(_('Adresát'), max_length=128)  # CHECK nebylo by lepsi pouzit EmailField
#     text_content = models.TextField(_('Textový obsah'))
#     html_content = models.TextField(_('HTML obsah'))
#     attachment_name = models.CharField(_('Název přílohy'), max_length=255)
#
#     class Meta:
#         verbose_name = _(u'Email')
#         verbose_name_plural = _(u'Emaily')


class EmailAttachment(object):
    """
    Object for handling attachments to emails.
    :param path: full path of the file on the disk
    :param mimetype: mimetype of the file (optional, can be guessed by Django)
    """
    path = ''
    mimetype = ''

    def __init__(self, path, mimetype=None):
        self.path = path
        self.mimetype = mimetype
