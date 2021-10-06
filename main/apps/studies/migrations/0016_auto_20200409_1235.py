# Generated by Django 3.0 on 2020-04-09 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0005_auto_20200329_1914'),
        ('studies', '0015_auto_20200408_1053'),
    ]

    operations = [
        migrations.AddField(
            model_name='study',
            name='billing_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='study',
            name='closed_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='study',
            name='prelaunched_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='study',
            name='progress_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='study',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='studies', to='companies.Company'),
        ),
    ]