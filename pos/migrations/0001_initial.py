# Generated by Django 4.1.4 on 2022-12-14 06:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='sales_transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_type', models.CharField(choices=[('CASH', 'CASH'), ('CREDIT', 'CREDIT'), ('CARDS', 'CARDS'), ('NETS', 'NETS'), ('GRAB', 'GRAB'), ('OTHERS', 'OTHERS')], max_length=25)),
                ('grand_total', models.DecimalField(decimal_places=2, max_digits=21)),
                ('remarks', models.TimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='sales_services',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=350)),
                ('service_price', models.DecimalField(decimal_places=2, max_digits=21)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('sales_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.sales_transaction')),
            ],
        ),
    ]
