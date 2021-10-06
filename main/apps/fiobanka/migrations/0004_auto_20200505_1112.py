# Generated by Django 3.0 on 2020-05-05 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fiobanka', '0003_auto_20190517_0833'),
    ]

    operations = [
        migrations.AddField(
            model_name='fiobanktransactions',
            name='processed_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='fiobanktransactions',
            name='transaction_id',
            field=models.CharField(max_length=15, unique=True, verbose_name='ID Transakce'),
        ),
    ]
