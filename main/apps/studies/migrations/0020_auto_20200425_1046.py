# Generated by Django 3.0 on 2020-04-25 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0019_auto_20200423_1337'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpatient',
            name='street_number',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='street_number'),
        ),
        migrations.AddField(
            model_name='patient',
            name='street_number',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='street_number'),
        ),
    ]
