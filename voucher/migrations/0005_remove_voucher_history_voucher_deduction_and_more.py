# Generated by Django 4.1.4 on 2022-12-28 05:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('voucher', '0004_voucher_eachtime_voucher_grand_total_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='voucher_history',
            name='voucher_deduction',
        ),
        migrations.AddField(
            model_name='voucher_history',
            name='type',
            field=models.CharField(blank=True, choices=[('CREDIT', 'CREDIT'), ('DEBIT', 'DEBIT')], default=None, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='voucher_history',
            name='voucher_amount',
            field=models.IntegerField(default=0),
        ),
    ]
