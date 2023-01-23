from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from base.views import LoginView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    path('', views.appointmentOverview, name="appointment-overview"),
    path('search/', views.appointmentSearch, name="appointment-search"),
    path('create/', views.appointmentCreate, name="appointment-create"),
    path('calendar/', views.appointmentCalendar, name="appointment-calendar"),

    #employee set date slot
    path('set/availdate', views.setAvailDate, name="appointment-setDate"),
    #toogle dates for employee
    path('set/toogleDates', views.toogleDatesEmployee, name="appointment-toogleDates"),

    #user book new appointment
    path('new/appointment', views.userNewAppointment, name="appointment-userNewAppointment"),
    #get employee dates AJAX
    path('new/appointment/edate', views.get_employee_dates, name="appointment-edate"),
    #get employee time AJAX
    path('new/appointment/etime', views.get_employee_time, name="appointment-etime"),
    #get employee services AJAX
    path('new/appointment/eservice', views.get_employee_service, name="appointment-eservice"),
    #get econfirm AJAX
    path('new/appointment/econfirm', views.get_econfirm, name="appointment-econfirm"),
    #book appointment (user perspective)
    path('new/appointment/ebook', views.userBookAppointment, name="appointment-ebook"),
    #Change appointment status ADMIN only
    path('new/appointment/changeappstatus', views.changeAppointmentStatus, name="appointment-changeAppStatus"),
    #check customer phone number AJAX ADMIN only
    path('new/appointment/checkphone', views.searchCustomerPhone, name="appointment-checkphone"),

]