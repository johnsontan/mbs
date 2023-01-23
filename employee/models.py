from django.db import models
from base.models import userInfo as User
from django.utils import timezone

# Create your models here.

class employee_info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    sg_address = models.TextField(blank=True, null=True)
    my_address = models.TextField(blank=True, null=True)
    wp_id = models.TextField(blank=True, null=True)
    inner_role = models.CharField(blank=True, null=True, max_length=100)
    created_at = models.DateTimeField(default=timezone.now)

class employee_avail_leaves(models.Model):
    days_available = models.IntegerField(default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

class employee_leaves_history(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    approve = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


