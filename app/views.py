from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from .models import Course, UserProfile
from .forms import CustomUserCreationForm, UserProfileForm, UserForm, LoginForm, Create_course_Form, Build_faceForm

# Create your views here.

def hello_world(request):
    a = 10
    b = 5
    s = a + b
    d = a - b
    p = a * b
    q = a / b
    return render(request, 'hello_world.html',locals())

def home(request):
    course_list = Course.objects.all()
    context = {
        'course_list': course_list
    }
    if request.user.is_authenticated :
        return render(request, 'check_in/home_out.html', context)
    else : 
        return render(request, 'check_in/home_in.html', context)

def create_course(request):
    if request.method == 'POST':
        form = Create_course_Form(request.POST)
        if form.is_valid():
            course = form.save()
            return redirect(course.get_absolute_url())
    else:
        form = Create_course_Form()

    return render(request, 'check_in/create_course.html', {'form': form})

def registration(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("check_in:Login"))

    context = {
        'form': form
    }
    return render(request, 'check_in/registration.html', context)

def build_face(request):
    form = Build_faceForm()
    if request.method == "POST":
        form = Build_faceForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            return render(request, 'check_in/show.html', {'data' : data})

    context = {
        'form': form
    }
    return render(request, 'check_in/build_face.html', context)

def log_in(request):
    form = LoginForm()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse("check_in:profile"))  #重新導向到首頁
    context = {
        'form': form
    }
    return render(request, 'check_in/login.html', context)

def log_out(request):
    logout(request)
    return redirect(reverse("check_in:Login"))

def course_profile(request, id):
    course = get_object_or_404(Course, id = id)
    students_list = course.students.all()
    teachers_list = course.teacher.all()
    context = {
        'course' : course,
        'teacher_list' : teachers_list,
        'student_list' : students_list
    }
    return render(request, "check_in/course_profile.html", context)

@login_required
def profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    print(request.user.last_name)
    context = {
        'form1' : request.user,#UserForm(instance=request.user),
        'form2' : profile,#UserProfileForm(instance=profile),
        'course_list' : request.user.students.all()
    }
    return render(request, 'check_in/profile.html', context)
        