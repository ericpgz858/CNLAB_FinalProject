"""
URL configuration for CNL_FJ project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from . import views
app_name = 'check_in'
urlpatterns = [
    path('', views.hello_world, name='begining'),
    path('home/', views.home, name='home'),
    path('Login/', views.log_in, name='Login'),
    path('Logout/', views.log_out, name='Logout'),
    path('registration/', views.registration, name='registration'),
    path('create/', views.create_course, name='create_course'),
    path('course_<int:id>/', views.course_profile, name='course_profile'),
    path('profile/', views.profile, name='profile'),
    path('build/', views.build_face, name='build_face'),
]