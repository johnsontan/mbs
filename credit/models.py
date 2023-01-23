from django.db import models
from django.utils import timezone
from base.models import userInfo as User
from pos.models import sales_transaction

# Create your models here.

class credits(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE, primary_key=True)
    balance = models.DecimalField(max_digits=21, decimal_places=2, default="0.00")
    created_at = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)

class credits_history(models.Model):
    TYPE_CHOICES = (
        ("CREDIT", "CREDIT"),
        ("DEBIT", "DEBIT")
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=21, decimal_places=2)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=None, blank=True, null=True)
    transaction = models.OneToOneField(sales_transaction, on_delete=models.CASCADE, null=True, blank=True)
    remarks =models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_update = models.DateTimeField(default=timezone.now)
