# Generated by Django 3.0 on 2020-05-25 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_paycheckgeneration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='total_value',
            field=models.BigIntegerField(),
        ),
    ]