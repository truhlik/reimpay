# Generated by Django 3.0 on 2020-09-02 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0042_arm_d_visit_items_cost'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalstudy',
            name='operator',
            field=models.CharField(choices=[('CRO', 'CRO'), ('SPONSOR', 'CRO')], default='SPONSOR', max_length=32, verbose_name='study operator'),
        ),
        migrations.AddField(
            model_name='historicalstudy',
            name='sponsor_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Sponsor name'),
        ),
        migrations.AddField(
            model_name='study',
            name='operator',
            field=models.CharField(choices=[('CRO', 'CRO'), ('SPONSOR', 'CRO')], default='SPONSOR', max_length=32, verbose_name='study operator'),
        ),
        migrations.AddField(
            model_name='study',
            name='sponsor_name',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Sponsor name'),
        ),
    ]
