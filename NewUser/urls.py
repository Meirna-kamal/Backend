from allauth.account.views import confirm_email
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from .views import Login

urlpatterns = [
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'registration/', include('rest_auth.registration.urls')),
    url(r'^account/', include('allauth.urls')),
    url(r'^confirm-email/(?P<key>.+)/$', confirm_email, name='account_confirm_email'),
]