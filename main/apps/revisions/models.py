from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.dispatch import receiver
from django.contrib.postgres.fields import JSONField

from simple_history.signals import post_create_historical_record

from main.libraries.models import BaseModel


def get_diff_data(history_instance):
    prev_record = history_instance.prev_record
    if prev_record is None:
        return None

    data = []
    delta = history_instance.diff_against(prev_record)
    for change in delta.changes:
        data.append({
            'field': change.field,
            'old': str(getattr(delta.old_record, change.field)),
            'new': str(getattr(delta.new_record, change.field))
        })
    return data


@receiver(post_create_historical_record)
def post_create_historical_record_callback(sender, instance, history_instance, history_date, history_change_reason,
                                           history_user, using, **kwargs):
    data = get_diff_data(history_instance)

    actions = {
        '-': 'deleted',
        '+': 'created',
        '~': 'updated',
    }
    action = actions.get(history_instance.history_type)
    if action == 'updated' and not data:
        return

    if action == 'deleted':
        return

    obj = AuditLog(
        user=history_user,
        content_type=ContentType.objects.get_for_model(instance),
        object_id=instance.id,
        obj_name=str(instance),
        update_data=data,
        action=action,
        study_id=instance.get_group_obj_id(),
    )
    obj.save()


# todo denormalizovat uživatelské jméno při smazání uživatele
# todo updatovat denormalizované jméno objektu
class AuditLog(BaseModel):
    user = models.ForeignKey('users.User', related_name='+', on_delete=models.SET_NULL, blank=True, null=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    content_object = GenericForeignKey('content_type', 'object_id')
    obj_name = models.CharField(max_length=255)
    action = models.CharField(max_length=32)
    update_data = JSONField(default=dict, null=True)
    study = models.ForeignKey('studies.Study', related_name='logs', on_delete=models.CASCADE)
