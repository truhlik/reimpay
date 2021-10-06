# Generated by Django 3.0 on 2020-04-07 12:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('studies', '0008_auto_20200329_1943'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalPatient',
            fields=[
                ('id', models.IntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('number', models.CharField(max_length=255, verbose_name='Randomisation')),
                ('payment_type', models.CharField(choices=[('BANK', 'bank transfer'), ('POST', 'czech Post payment order (cash)')], max_length=32, verbose_name='payment form')),
                ('payment_info', models.CharField(max_length=255, verbose_name='payment info')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField()),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('arm', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='studies.Arm', verbose_name='arm')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('study', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='studies.Study', verbose_name='study')),
            ],
            options={
                'verbose_name': 'historical patient',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': 'history_date',
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Vytvořeno')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Upraveno')),
                ('number', models.CharField(max_length=255, verbose_name='Randomisation')),
                ('payment_type', models.CharField(choices=[('BANK', 'bank transfer'), ('POST', 'czech Post payment order (cash)')], max_length=32, verbose_name='payment form')),
                ('payment_info', models.CharField(max_length=255, verbose_name='payment info')),
                ('arm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patients', to='studies.Arm', verbose_name='arm')),
                ('study', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='patients', to='studies.Study', verbose_name='study')),
            ],
            options={
                'verbose_name': 'patient',
                'verbose_name_plural': 'patients',
                'unique_together': {('study', 'number')},
            },
        ),
    ]