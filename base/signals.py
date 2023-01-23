from django.db.models.signals import post_save
from .models import userInfo, profile_pic
from employee.models import employee_info
from credit.models import credits
from django.dispatch import receiver


@receiver(post_save, sender=userInfo)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile_pic.objects.create(user=instance)
        credits.objects.create(user=instance, balance=0)
        if instance.role == 2:
            employee_info.objects.create(user=instance)


@receiver(post_save, sender=userInfo)
def save_profile(sender, instance, **kwargs):
    instance.profile_pic.save()
    instance.credits.save()
    try:
        if instance.employee_info:
            instance.employee_info.save()
    except:
        pass