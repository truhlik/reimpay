# Generated by Django 3.0 on 2020-03-21 17:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0003_auto_20200319_1054'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='users',
        ),
        migrations.DeleteModel(
            name='UserCompany',
        ),
    ]
