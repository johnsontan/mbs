from django.db import models
from django.utils import timezone
from base.models import userInfo as User
from pos.models import sales_transaction
from jsignature.fields import JSignatureField
from jsignature.mixins import JSignatureFieldsMixin


# Create your models here.

class voucher(models.Model):
    voucher_name = models.CharField(max_length=350)
    qty = models.IntegerField(default=1)
    tqty = models.IntegerField(default=1)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    grand_total = models.DecimalField(max_digits=21, decimal_places=2, default="0.00")
    eachtime = models.DecimalField(max_digits=21, decimal_places=2, default="0.00")
    created_at = models.DateTimeField(default=timezone.now)

class voucher_history(models.Model):
    TYPE_CHOICES = (
        ("CREDIT", "CREDIT"),
        ("DEBIT", "DEBIT")
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    voucher = models.ForeignKey(voucher, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=None, blank=True, null=True)
    voucher_amount = models.IntegerField(default=0)
    sales_transaction = models.ForeignKey(sales_transaction, on_delete=models.CASCADE, blank=True, null=True)
    signature = JSignatureField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
