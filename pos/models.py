from django.db import models
from base.models import userInfo as User
from django.utils import timezone

# Create your models here.

class sales_transaction(models.Model):
    PAYMENT_TYPE = (
        ("CASH", "CASH"),
        ("CREDIT", "CREDIT"),
        ("CARDS", "CARDS"),
        ("NETS", "NETS"),
        ("GRAB","GRAB"),
        ("OTHERS", "OTHERS")
    )
    payment_type = models.CharField(max_length=25, choices=PAYMENT_TYPE, blank=False, null=False)
    grand_total = models.DecimalField(max_digits=21, decimal_places=2)
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employee')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer', null=True, blank=True)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

class sales_services(models.Model):

    DEPARTMENTS = (
        ("HAIR", "HAIR"),
        ("BEAUTY", "BEAUTY"),
        ("HAIR PRODUCT", "HAIR PRODUCT"),
        ("BEAUTY PRODUCT", "BEAUTY PRODUCT")

    )

    service_name = models.CharField(max_length=350)
    service_price = models.DecimalField(max_digits=21, decimal_places=2)
    service_department = models.CharField(max_length=25, choices=DEPARTMENTS, default="HAIR")
    sales_id = models.ForeignKey(sales_transaction, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
