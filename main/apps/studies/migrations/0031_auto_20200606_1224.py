# Generated by Django 3.0 on 2020-06-06 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0030_auto_20200525_1340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='study',
            name='variable_symbol',
            field=models.PositiveIntegerField(blank=True, max_length=255, null=True),
        ),
    ]
