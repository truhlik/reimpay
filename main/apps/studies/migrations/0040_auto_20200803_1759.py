# Generated by Django 3.0 on 2020-08-03 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0039_auto_20200722_1120'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientvisititem',
            name='payment_status',
            field=models.CharField(choices=[('WAITING', 'In enque for processing'), ('SENT', 'Sent'), ('RETURNED', 'Returned')], default='WAITING', max_length=32, null=True),
        ),
    ]
