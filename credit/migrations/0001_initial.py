# Generated by Django 4.1.4 on 2022-12-14 06:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pos', '__first__'),
        ('base', '0002_alter_userinfo_role'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='credits',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('balance', models.DecimalField(decimal_places=2, default='0.00', max_digits=21)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('last_update', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='credits_history',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=21)),
                ('type', models.CharField(blank=True, choices=[('CREDIT', 'CREDIT'), ('DEBIT', 'DEBIT')], default=None, max_length=20, null=True)),
                ('transaction', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pos.sales_transaction')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
