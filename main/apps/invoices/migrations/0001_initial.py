# Generated by Django 3.0 on 2020-06-02 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('companies', '0006_company_fa_subject_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Vytvořeno')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Upraveno')),
                ('fakturoid_invoice_id', models.IntegerField()),
                ('fakturoid_public_url', models.URLField()),
                ('invoice_number', models.CharField(max_length=255)),
                ('issue_date', models.DateField()),
                ('amount', models.PositiveIntegerField()),
                ('status', models.CharField(choices=[('ISSUED', 'Issued'), ('PAID', 'Paid'), ('CANCELLED', 'Cancelled')], default='ISSUED', max_length=32)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='companies.Company')),
            ],
            options={
                'verbose_name': 'invoice',
                'verbose_name_plural': 'invoices',
            },
        ),
    ]
