# Generated by Django 3.0 on 2020-05-27 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0005_remove_creditbalance_custom_fk_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditbalance',
            name='commission',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='credit_balances', to='credit.CreditBalance'),
        ),
    ]
