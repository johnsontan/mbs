# Generated by Django 4.1.4 on 2022-12-27 07:37

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('credit', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='credits_history',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='credits_history',
            name='last_update',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
