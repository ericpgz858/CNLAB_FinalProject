from django.contrib import admin
from django.urls import path, include

from . import views
app_name = 'main'
urlpatterns = [
    path('home', views.home, name='home'),
    path('login/', views.log_in, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('registration/', views.registration, name='registration'),
    path('create/', views.create_course, name='create_course'),
    path('course_<int:id>/', views.course_profile, name='course_profile'),
    path('profile_<int:id>/', views.profile, name='profile'),
    path('history_divide_<int:id>/', views.history_divide, name='history_divide'),
    path('history_<int:course_id>_<int:student_id>/', views.history, name='history'),
    path('test/', views.sign_in, name='test'),
    path('face_detect_<int:course_id>', views.face_detect, name='face_detect'),
    path('face_build', views.face_build, name='face_build'),
    path('download_<int:course_id>', views.Downloadcourse, name = 'download')
]
