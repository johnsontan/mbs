from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    path('', views.voucherOverview, name="voucher-overview"),
    path('credit/', views.voucherCredit, name="voucher-credit"),
    path('debit/', views.voucherDebit, name="voucher-debit"),
    path('search/', views.voucherSearch, name="voucher-search"),

    #Find customer vouchers AJAX
    path('customer/vouchers', views.findCustomerVoucher, name="voucher-customerVoucher"),
]