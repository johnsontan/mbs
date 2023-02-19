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
    #detail-services
    #HIAR
    path('service/hair/mucota-rebond', views.serviceHairMucotaRebond, name='base-service-hair-mucota-rebond'),
    path('service/hair/botox-straight', views.serviceHairBotoxStraight, name='base-service-hair-botox-straight'),
    path('service/hair/botox-repair', views.serviceHairBotoxRepair, name='base-service-hair-botox-repair'),
    path('service/hair/keratin-treatment', views.serviceHairKeratinTreatment, name='base-service-hair-keratin-treatment'),
    path('service/hair/keratin-qod-treatment', views.serviceHairKeratinQodTreatment, name='base-service-hair-keratin-qod-treatment'),
    path('service/hair/essential-hair-treatment', views.serviceHairEssentialHairTreatment, name='base-service-hair-essential-hair-treatment'),
    path('service/hair/essential-scalp-treatment', views.serviceHairEssentialScalpTreatment, name='base-service-hair-essential-scalp-treatment'),
    path('service/hair/protien-hair-treatment', views.serviceHairProtienHairTreatment, name='base-service-hair-protien-hair-treatment'),
    path('service/hair/revivify-hair-treatment', views.serviceHairRevivifyHairTreamtent, name='base-service-hair-revivify-hair-treatment'),
    path('service/hair/detoxify-scalp-treatment', views.serviceHairDetoxifyScalpTreatment, name='base-service-detoxify-scalp-treatment'),
    path('service/hair/tcm-scalp-treatment', views.serviceHairTcmScalpTreatment, name='base-service-hair-tcm-scalp-treatment'),
    #BEAUTY
    path('service/beauty/organic-refreshing-facial', views.serviceBeautyOrganicRefreshingFacial, name='base-service-beauty-organic-refreshing-facial'),
    path('service/beauty/organic-stem-cell-facial', views.serviceBeautyOrganicStemCellFacial, name='base-service-beauty-organic-stem-cell-facial'),
    path('service/beauty/purifying-facial', views.serviceBeautyPurifyingFacial, name='base-service-beauty-purifying-facial'),
    path('service/beauty/Co2-peel-oxyglow-facial', views.serviceBeautyCO2PeelOxyglowFacial, name='base-service-beauty-Co2-peel-oxyglow-facial'),
    path('service/beauty/aromatic-age-reverse-facial', views.serviceBeautyAromaticAgeReverseFacial, name='base-service-beauty-aromatic-age-reverse-facial'),
    path('service/beauty/intensive-hydrating-facial', views.serviceBeautyIntensiveHydratingFacial, name='base-service-beauty-intensive-hydrating-facial'),
    path('service/beauty/rejuvenate-eye-treatment', views.serviceBeautyRejuvenateEyeTreatment, name='base-service-beauty-rejuvenate-eye-treatment'),
    path('service/beauty/intensive-eye-treatment', views.serviceBeautyIntensiveEyeTreatment, name='base-service-beauty-intensive-eye-treatment'),


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
