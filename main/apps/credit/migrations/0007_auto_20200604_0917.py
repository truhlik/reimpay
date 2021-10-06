# Generated by Django 3.0 on 2020-06-04 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0006_creditbalance_commission'),
    ]

    operations = [
        migrations.AddField(
            model_name='creditbalance',
            name='item_amount',
            field=models.IntegerField(default=0, verbose_name='bez DPH'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='creditbalance',
            name='vat_amount',
            field=models.IntegerField(blank=True, default=0, verbose_name='DPH'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='creditbalance',
            name='vat_rate',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='procentuální sazba DPH'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='creditbalance',
            name='balance_amount',
            field=models.IntegerField(blank=True, verbose_name='suma'),
        ),
        migrations.AlterField(
            model_name='creditbalance',
            name='balance_sum',
            field=models.IntegerField(blank=True, verbose_name='sumarizace kreditu'),
        ),
    ]