from django.contrib import admin

# Register your models here.
from .models import Course, UserProfile

# Register your models here.
admin.site.register(Course)
admin.site.register(UserProfile)

