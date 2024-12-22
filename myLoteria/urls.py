from django.urls import path, include
from django.urls import re_path 
from myLoteria import views

urlpatterns = [
    re_path(r'^home/', views.home, name='home'),
    path("accounts/", include('django.contrib.auth.urls')),
    path('index/', views.index, name='index'),
    re_path('', views.home, name='home'),
]
