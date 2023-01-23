from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    path('', views.managerIndex, name="manager-home"),

    #users
    path('useroverview/', views.userOverview, name="manager-userOverview"),
    path('usersearch/', views.userSearch, name="manager-userSearch"),
    path('usercreate/', views.userCreate, name="manager-userCreate"),
    #USER UPDATE ROUTES
    path('user/update', views.userSearchUpdate, name="manager-userSearchUpdate"),
    path('user/suspend', views.userSuspendToogle, name="manager-userSuspendToogle"),
    path('user/sendNotificaiton', views.userSendNotification, name="manager-userSendNotification"),

    #services
    path('serviceoverview/', views.serviceOverview, name="manager-serviceOverview"),
    path('servicecreate/', views.serviceCreate, name="manager-serviceCreate"),
    path('serviceEdit/', views.serviceEdit, name="manager-serviceEdit"),
    path('serviceEditUpdate/', views.serviceEditUpdate, name="manager-serviceEditUpdate"),

    #contact overview
    path('contact/overview/', views.contactOverview, name="manager-contactOverview"),

    #news
    path('news/overview/', views.newsOverview, name="manager-newsOverview"),
    path('news/create/', views.newsCreate, name="manager-newsCreate"),
    path('news/edit/', views.newsEdit, name="manager-newsEdit"),
    path('news/editUpdate/', views.newsEditUpdate, name="manager-newsEditUpdate"),

    #testimonal 
    path('testimonal/overview/', views.testimonialPicOverview, name="manager-testimonalOverview"),
    path('testimonal/create/', views.createTestimonialPic, name="manager-testimonialCreate"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
