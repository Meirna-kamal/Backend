from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
urlpatterns=[
    path('signIn/',auth_views.LoginView.as_view(template_name='signIn/signIn.html'),name='signIn')]