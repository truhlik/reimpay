# Generated by Django 3.0 on 2020-04-29 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0024_auto_20200425_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalvisit',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='visit',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='title'),
        ),
    ]
