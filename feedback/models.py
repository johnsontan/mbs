from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class feedback(models.Model):
    friendliness = models.IntegerField(blank=False, null=False)
    cleaniness = models.IntegerField(blank=False, null=False)
    price_satisfaction = models.IntegerField(blank=False, null=False)
    service_satisfaction = models.IntegerField(blank=False, null=False)
    overall_satisfaction = models.IntegerField(blank=False, null=False)
    remarks = models.TextField(blank=False, null=False)
    name = models.CharField(max_length=150, blank=False, null=False)
    phone_number = models.IntegerField(blank=False, null=False)
