from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django import forms
from django.utils import timezone
import datetime
# Create your models here.

class Course(models.Model):
	course_name = models.CharField(max_length = 20)
	teacher = models.ManyToManyField(User, related_name = 'teachers')
	students = models.ManyToManyField(User, related_name = 'students')
	start_date = models.CharField(blank=True, max_length = 20)
	end_date = models.CharField(blank=True, max_length = 20)
	course_address = models.CharField(blank=True, max_length = 100)

	def get_absolute_url(self):
		return reverse("check_in:course_profile", kwargs={"id": self.id})


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # blank = true, 在用 form 填表單時可以不用填
    student_id = models.CharField(blank=True, max_length=20)
    department = models.CharField(blank=True, max_length=50)
    is_teacher = models.BooleanField(blank=True, default=False)
    is_student = models.BooleanField(blank=True, default=False)
    
class Image(models.Model):
	image = models.ImageField(upload_to='image/', blank=True, null=True)
	student_id = models.CharField(blank=True, max_length=20)