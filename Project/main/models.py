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
		return reverse("main:course_profile", kwargs={"id": self.id})
	
	def get_class_signin_url(self):
		return reverse("main:face_detect", kwargs={"course_id": self.id})
	
	def get_his_div_url(self):
		return reverse("main:history_divide", kwargs={"id": self.id})
	
	def get_signin_test_url(self):
		return 'http://35.78.57.63:8000/?class='+self.course_name+'&clsss_id='+self.id
	
	def get_download_csvfile(self):
		return reverse("main:download", kwargs={"course_id": self.id})


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # blank = true, 在用 form 填表單時可以不用填
    student_id = models.CharField(blank=True, max_length=20)
    department = models.CharField(blank=True, max_length=50)
    is_teacher = models.BooleanField(blank=True, default=False)
    is_student = models.BooleanField(blank=True, default=False)
    
    def get_absolute_url(self):
	    return reverse("main:profile", kwargs={"id": self.id})
    
class Image(models.Model):
	image = models.ImageField(upload_to='image/', blank=True, null=True)
	student_id = models.CharField(blank=True, max_length=20)
