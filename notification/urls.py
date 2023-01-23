from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('overview/', views.notificationOverview, name="notification-overview"),
    path('new/', views.notificationsend, name="notification-send"),
    path('search/', views.notificationSearch, name="notification-search"),

]