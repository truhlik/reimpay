# Generated by Django 3.0 on 2020-03-17 20:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0002_auto_20191223_1543'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Email',
        ),
        migrations.DeleteModel(
            name='SMS',
        ),
    ]
