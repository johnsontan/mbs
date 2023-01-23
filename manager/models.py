from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField 
from PIL import Image

# Create your models here.

class services(models.Model):
    service_name = models.CharField(max_length=300)
    service_description = models.TextField(blank=True, null=True)
    service_tnc = models.TextField(blank=True, null=True)
    service_price = models.DecimalField(max_digits=21, decimal_places=2)
    department = models.CharField(blank=True, null=True, max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

class image_links(models.Model):
    image_url = models.URLField()
    image_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

class news(models.Model):
    news_title = models.CharField(max_length=250)
    news_description = RichTextField()
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

class testimonial_pic(models.Model):
    image = models.ImageField(default='default.png', upload_to='testimonal_pics')
    name = models.CharField(max_length=250, default="Nil", blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Image created at {self.created_at}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 900 or img.width > 1200:
            output_size = (900,1200)
            img.thumbnail(output_size)
            img.save(self.image.path)

