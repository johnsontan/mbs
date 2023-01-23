# Generated by Django 4.1.4 on 2022-12-15 09:41

import base.models
import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_alter_userinfo_role'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='userinfo',
            managers=[
                ('object', base.models.UserManager()),
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='username',
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='email address'),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='role',
            field=models.PositiveBigIntegerField(choices=[(2, 'Employee'), (1, 'Customer'), (3, 'Assistant'), (4, 'Manager')], default='1'),
        ),
    ]
