# Generated by Django 3.0 on 2020-04-25 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0020_auto_20200425_1046'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpatient',
            name='change_payment_request',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='patient',
            name='change_payment_request',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
