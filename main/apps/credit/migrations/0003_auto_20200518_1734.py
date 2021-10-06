# Generated by Django 3.0 on 2020-05-18 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0001_initial'),
        ('credit', '0002_auto_20200505_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditbalance',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='credit_balances', to='payments.Payment'),
        ),
        migrations.AlterField(
            model_name='creditbalance',
            name='balance_type',
            field=models.CharField(choices=[('TOPUP', 'TOPUP'), ('COMMISSION', 'COMMISSION'), ('PATIENT_PAYCHECK', 'PATIENT_PAYCHECK'), ('BANK_TRANSFER_FEE', 'BANK_TRANSFER_FEE'), ('POST_OFFICE_FEE', 'POST_OFFICE_FEE')], max_length=32, verbose_name='typ pohybu'),
        ),
    ]