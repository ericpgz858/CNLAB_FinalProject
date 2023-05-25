from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Course, UserProfile, Image

BOOL_CHOICES = ((True, 'Yes'), (False, 'No'))

class Create_course_Form(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'email']
	
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['student_id', 'department'] 
	
class CustomUserCreationForm(UserCreationForm):
	username = forms.CharField(
		label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
	lastname = forms.CharField(
		label="姓氏",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
	firstname = forms.CharField(
		label="名字",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
	identity_option = forms.ChoiceField(
		label="身分",
        choices=[('is_teacher', '老師'), ('is_student', '學生')], 
        widget=forms.RadioSelect(choices=BOOL_CHOICES)
    )
	department = forms.CharField(
        label="學系",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
	email = forms.EmailField(
        label="電子郵件",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
	password1 = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
	password2 = forms.CharField(
        label="密碼確認",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
	class Meta:
		model = User
		fields = ('username', 'lastname', 'firstname', 'identity_option', 'department', 'email', 'password1', 'password2')
		
	def save(self, commit=True):
		user = super().save(commit=False)
		#save(commit=False) The most common situation is to get the instance from form 
		#but only 'in memory', not in database.
		
		# Modify user data
		user.first_name = self.cleaned_data['firstname']
		user.last_name = self.cleaned_data['lastname']
		
		if commit:
			user.save()
			# Access and modify user data through the user model
			profile = UserProfile.objects.get_or_create(user=user)[0]
			profile.student_id = 'None'
			profile.department = self.cleaned_data['department']
			print(self.cleaned_data)
			if self.cleaned_data['identity_option'] == 'is_teacher' : 
				profile.is_teacher = True
				profile.is_student = False
			else :
				profile.is_teacher = False
				profile.is_student = True
				profile.student_id = self.cleaned_data['username']
			profile.save()
		
		return user
	
class LoginForm(forms.Form):
    username = forms.CharField(
        label="帳號",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="密碼",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    
class Build_faceForm(forms.Form):
    student_id = forms.CharField(
        label="學號",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = '__all__'