from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from base.views import LoginView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.index, name='base-home'),
    path('test/', views.test, name='base-test'),

    #Authentication 
    path('register/', views.register_user, name='base-register'),
    path('login/', views.LoginView, name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='base/index.html'), name='logout'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='base/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="base/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='base/password_reset_complete.html'), name='password_reset_complete'),
    path("password_reset/", views.password_reset_request, name="password_reset"),

    #PROFILE 
    path('profile/', views.profile, name="base-profile"),

    #notification
    path('profile/ack/notification/', views.notification_ack, name="base-ackNotification"),

    #Services
    path('service/beauty', views.serviceBeauty, name='base-service-beauty'),
    path('service/hair', views.serviceHair, name='base-service-hair'),

    #about us
    path('aboutus/', views.aboutus, name="base-aboutus"),

    #contact
    path('contact/', views.contact, name="base-contact"),

    #news
    path('news/', views.newsOverview, name="base-newsOverview"),
    path('news/more', views.innerNews, name="base-innerNews"),

    #GET more appointment information AJAX
    path('profile/moreappinfo', views.moreAppInformation, name="base-moreappinfo"),
    #GET latest news AJAX
    path('getnews/', views.getNews, name="base-getNews"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
