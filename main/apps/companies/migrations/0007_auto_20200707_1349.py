# Generated by Django 3.0 on 2020-07-07 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0006_company_fa_subject_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='web',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='web'),
        ),
    ]
