# Generated by Django 3.0 on 2020-03-22 10:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0004_auto_20200321_1733'),
        ('studies', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='study',
            name='company',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, related_name='studies', to='companies.Company'),
            preserve_default=False,
        ),
    ]
