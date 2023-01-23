from django.contrib import admin
from .models import userInfo, profile_pic

# Register your models here.

admin.site.register(userInfo)
admin.site.register(profile_pic)
