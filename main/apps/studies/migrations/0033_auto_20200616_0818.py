# Generated by Django 3.0 on 2020-06-16 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0032_auto_20200616_0750'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalpatient',
            name='number',
            field=models.CharField(max_length=255, verbose_name='randomisation'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='number',
            field=models.CharField(max_length=255, verbose_name='randomisation'),
        ),
    ]