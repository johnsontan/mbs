from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    path('', views.posStart, name='pos-start'),
    path('earnings/', views.posEarnings, name='pos-earnings'),
    path('receipt/', views.posReceipt, name='pos-receipt'),

    #submit transaction
    path('transact/', views.posTransact, name='pos-tranasct'),
    #Get all services per transaction AJAX
    path('transaction/getservices', views.rservice, name='pos-getServices'),
    
]