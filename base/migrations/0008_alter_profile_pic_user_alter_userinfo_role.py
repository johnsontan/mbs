# Generated by Django 4.1.4 on 2022-12-16 05:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_alter_userinfo_role_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile_pic',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='role',
            field=models.PositiveBigIntegerField(choices=[(3, 'Assistant'), (1, 'Customer'), (4, 'Manager'), (2, 'Employee')], default='1'),
        ),
    ]
