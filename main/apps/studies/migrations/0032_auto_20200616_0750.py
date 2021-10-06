# Generated by Django 3.0 on 2020-06-16 07:50

from django.db import migrations, models
import encrypted_fields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0031_auto_20200606_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpatient',
            name='city',
            field=encrypted_fields.fields.EncryptedCharField(blank=True, max_length=255, null=True, verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='historicalpatient',
            name='name',
            field=encrypted_fields.fields.EncryptedCharField(blank=True, max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='historicalpatient',
            name='number',
            field=encrypted_fields.fields.EncryptedCharField(max_length=255, verbose_name='randomisation'),
        ),
        migrations.AlterField(
            model_name='historicalpatient',
            name='payment_info',
            field=encrypted_fields.fields.EncryptedCharField(blank=True, max_length=255, null=True, verbose_name='payment info'),
        ),
        migrations.AlterField(
            model_name='historicalpatient',
            name='street',
            field=encrypted_fields.fields.EncryptedCharField(blank=True, max_length=255, null=True, verbose_name='street'),
        ),
        migrations.AlterField(
            model_name='historicalpatient',
            name='street_number',
            field=encrypted_fields.fields.EncryptedCharField(blank=True, max_length=255, null=True, verbose_name='street_number'),
        ),
        migrations.AlterField(
            model_name='historicalpatient',
            name='zip',
            field=encrypted_fields.fields.EncryptedCharField(blank=True, max_length=255, null=True, verbose_name='zip'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='city',
            field=encrypted_fields.fields.EncryptedCharField(blank=True, max_length=255, null=True, verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='name',
            field=encrypted_fields.fields.EncryptedCharField(blank=True, max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='number',
            field=encrypted_fields.fields.EncryptedCharField(max_length=255, verbose_name='randomisation'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='payment_info',
            field=encrypted_fields.fields.EncryptedCharField(blank=True, max_length=255, null=True, verbose_name='payment info'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='street',
            field=encrypted_fields.fields.EncryptedCharField(blank=True, max_length=255, null=True, verbose_name='street'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='street_number',
            field=encrypted_fields.fields.EncryptedCharField(blank=True, max_length=255, null=True, verbose_name='street_number'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='zip',
            field=encrypted_fields.fields.EncryptedCharField(blank=True, max_length=255, null=True, verbose_name='zip'),
        ),
        migrations.AlterField(
            model_name='patientpaymentdata',
            name='city',
            field=encrypted_fields.fields.EncryptedCharField(blank=True, max_length=255, null=True, verbose_name='city'),
        ),
        migrations.AlterField(
            model_name='patientpaymentdata',
            name='name',
            field=encrypted_fields.fields.EncryptedCharField(blank=True, max_length=255, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='patientpaymentdata',
            name='payment_info',
            field=encrypted_fields.fields.EncryptedCharField(blank=True, max_length=255, null=True, verbose_name='payment info'),
        ),
        migrations.AlterField(
            model_name='patientpaymentdata',
            name='street',
            field=encrypted_fields.fields.EncryptedCharField(blank=True, max_length=255, null=True, verbose_name='street'),
        ),
        migrations.AlterField(
            model_name='patientpaymentdata',
            name='zip',
            field=encrypted_fields.fields.EncryptedCharField(blank=True, max_length=255, null=True, verbose_name='zip'),
        ),
        migrations.AlterField(
            model_name='study',
            name='variable_symbol',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
