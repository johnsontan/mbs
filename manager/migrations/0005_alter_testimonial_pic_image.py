# Generated by Django 4.1.4 on 2023-01-01 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0004_testimonial_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testimonial_pic',
            name='image',
            field=models.ImageField(default='default.png', upload_to='testimonal_pics'),
        ),
    ]
