from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    path('', views.employeeSearch, name="employee-search"),
    #save employee record
    path('save/employee/record', views.employeeInfoSave, name="employee-infoSave"),

]