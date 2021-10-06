from django.db import models
import uuid
from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sites', '0002_alter_domain_unique'),
    ]

    operations = [
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Vytvořeno')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Upraveno')),
                ('trash', models.BooleanField(default=False, verbose_name='Koš')),
                ('subject', models.CharField(max_length=255, verbose_name='Předmět')),
                ('email_from', models.CharField(max_length=128, verbose_name='Odesílatel')),
                ('email_to', models.CharField(max_length=128, verbose_name='Adresát')),
                ('text_content', models.TextField(verbose_name='Textový obsah')),
                ('html_content', models.TextField(verbose_name='HTML obsah')),
                ('attachment_name', models.CharField(max_length=255, verbose_name='Název přílohy')),
            ],
            options={
                'verbose_name': 'Email',
                'verbose_name_plural': 'Emaily',
            },
        ),
        migrations.CreateModel(
            name='SMS',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Vytvořeno')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Upraveno')),
                ('trash', models.BooleanField(default=False, verbose_name='Koš')),
                ('email_to', models.CharField(max_length=128, verbose_name='Adresát')),
                ('text_content', models.TextField(verbose_name='Textový obsah')),
            ],
            options={
                'verbose_name': 'SMS zpráva',
                'verbose_name_plural': 'SMS zprávy',
            },
        ),
    ]
