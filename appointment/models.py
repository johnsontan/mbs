from django.db import models
from PIL import Image
from django.utils import timezone, dateformat
from base.models import userInfo
from employee.models import employee_info
from manager.models import services

# Create your models here.
class appointment(models.Model):
    #choices
    UPCOMING = 1
    REJECTED = 2
    CANCEL = 3
    COMPLETE = 4
    MISSED =5

    STATUS_CHOICE = {
        (UPCOMING, "Upcoming"),
        (REJECTED, "Rejected"),
        (CANCEL, "Cancel"),
        (COMPLETE, "Complete"),
        (MISSED, "Missed")
    }

    user = models.ForeignKey(userInfo, blank=True, null=True, on_delete=models.CASCADE)
    appt_date = models.DateTimeField()
    employee = models.ForeignKey(employee_info, on_delete=models.CASCADE)
    status = models.CharField(max_length=1, choices=STATUS_CHOICE)
    created_at = models.DateTimeField(default=timezone.now)

class appointment_service(models.Model):
    appointment = models.ManyToManyField(appointment, blank=True, null=True)
    service = models.ManyToManyField(services, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

class appointment_available_dates(models.Model):
    employee = models.ForeignKey(userInfo, on_delete=models.CASCADE)
    avail_date = models.DateField()
    created_at = models.DateTimeField(default=timezone.now)

