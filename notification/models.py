from django.db import models
from django.utils import timezone
from base.models import userInfo as User

# Create your models here.

class notification(models.Model):
    notification_title = models.CharField(max_length=350)
    notification_description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

class ack_notification(models.Model):
    sent_user = models.ForeignKey(User, on_delete=models.CASCADE)
    sent_notification = models.ForeignKey(notification, on_delete=models.CASCADE)
    ack = models.DateTimeField(blank=True, null=True)
    
