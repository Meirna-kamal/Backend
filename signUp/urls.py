from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('signUp/',views.signUp,name='signUp'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
        
]