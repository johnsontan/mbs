"""mbs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('base.urls')),
    path('admin/', admin.site.urls),

    #manger routes
    path('mmanager/appointment/', include('appointment.urls')),
    path('mmanager/credit/', include('credit.urls')),
    path('mmanager/voucher/', include('voucher.urls')),
    path('mmanager/notification/', include('notification.urls')),
    path('mmanager/POS/', include('pos.urls')),
    path('mmanager/employee/', include('employee.urls')),
    path('mmanager/feedback/', include('feedback.urls')),
    path('mmanager/', include('manager.urls')),
    path('verification/', include('verify_email.urls')),	
]
