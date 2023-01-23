from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    path('', views.creditOverview, name="credit-overview"),
    path('cds/', views.creditCD, name="credit-CD"),
    path('search/', views.creditSearch, name="credit-search"),

    #Debit customer
    path('debitCustomer/', views.debitCustomer, name="credit-debitCustomer"),
    #Credit customer
    path('creditCustomer/', views.creditCustomer, name="credit-creditCustomer"),

]