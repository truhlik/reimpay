# Generated by Django 3.0 on 2020-04-24 17:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0019_auto_20200423_1337'),
        ('revisions', '0001_initial_new'),
    ]

    operations = [
        migrations.AddField(
            model_name='auditlog',
            name='group_obj',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='logs', to='studies.Study'),
            preserve_default=False,
        ),
    ]
