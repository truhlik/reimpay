# Generated by Django 3.0 on 2020-05-18 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0029_auto_20200507_1442'),
        ('credit', '0003_auto_20200518_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='creditbalance',
            name='reims',
            field=models.ManyToManyField(blank=True, related_name='credit_balances', to='studies.PatientVisitItem'),
        ),
    ]