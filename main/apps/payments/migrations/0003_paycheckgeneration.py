# Generated by Django 3.0 on 2020-05-25 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0030_auto_20200525_1340'),
        ('payments', '0002_payment_returned_on'),
    ]

    operations = [
        migrations.CreateModel(
            name='PaycheckGeneration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Vytvořeno')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Upraveno')),
                ('study', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paycheck_generations', to='studies.Study')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
