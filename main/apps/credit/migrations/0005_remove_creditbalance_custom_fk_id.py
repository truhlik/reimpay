# Generated by Django 3.0 on 2020-05-27 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0004_auto_20200518_1821'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='creditbalance',
            name='custom_fk_id',
        ),
    ]
