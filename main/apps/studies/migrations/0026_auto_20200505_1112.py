# Generated by Django 3.0 on 2020-05-05 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0025_auto_20200429_1124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arm',
            name='max_unscheduled',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='value'),
        ),
        migrations.AlterField(
            model_name='historicalarm',
            name='max_unscheduled',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='value'),
        ),
        migrations.AlterField(
            model_name='historicalsite',
            name='expected_patients',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Exp. patients'),
        ),
        migrations.AlterField(
            model_name='historicalstudyitem',
            name='price',
            field=models.PositiveSmallIntegerField(verbose_name='value'),
        ),
        migrations.AlterField(
            model_name='site',
            name='expected_patients',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='Exp. patients'),
        ),
        migrations.AlterField(
            model_name='studyitem',
            name='price',
            field=models.PositiveSmallIntegerField(verbose_name='value'),
        ),
    ]