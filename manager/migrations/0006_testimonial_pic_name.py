# Generated by Django 4.1.4 on 2023-01-02 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0005_alter_testimonial_pic_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='testimonial_pic',
            name='name',
            field=models.CharField(blank=True, default='Nil', max_length=250, null=True),
        ),
    ]
