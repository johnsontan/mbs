# Generated by Django 4.1.4 on 2022-12-15 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_userinfo_managers_remove_userinfo_username_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='role',
            field=models.PositiveBigIntegerField(choices=[(4, 'Manager'), (3, 'Assistant'), (2, 'Employee'), (1, 'Customer')], default='1'),
        ),
    ]
