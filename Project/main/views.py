from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from .models import Course, UserProfile
from .forms import CustomUserCreationForm, UserProfileForm, UserForm, LoginForm, Create_course_Form, AttendenceForm, Search_course_Form
# Create your views here.
#-----------------------------------------------------------------------------------------
from django.contrib.auth.models import User
import datetime
from .forms import   AttendenceForm
from django.http import HttpResponse
from .read_csv import *
import codecs
import pandas as pd
# 新增的 function

course_time_list = [[7, 10, 8, 0], 
                    [8, 10, 9, 0], 
                    [9, 10, 10, 0],
                    [10, 20, 11, 10],
                    [11, 20, 12, 10],
                    [12, 20, 13, 10],
                    [13, 20, 14, 10],
                    [14, 20, 15, 10],
                    [15, 30, 16, 20],
                    [16, 30, 17, 20],
                    [17, 30, 18, 20],
                    [18, 25, 19, 15],
                    [19, 20, 20, 10],
                    [20, 15, 21, 5],
                    [21, 10, 22, 0] ]
index_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '8', '10', 'A', 'B', 'C', 'D']
week_list = ["周一","周二","周三","周四","周五","周六","周日"]

def face_build(request):
    print(request.POST)
    return redirect("https://18.181.158.90:8502")

def face_detect(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    path = "https://18.181.158.90:8005/?class="+str(course_id)+"&classname="+course.course_name
    return redirect(path)

@login_required
def Downloadcourse(request, course_id):
    profile = get_object_or_404(UserProfile, user=request.user)
    course = get_object_or_404(Course, id = course_id)
    if profile.is_teacher:
        file_path = './csvfile/'+str(course_id)+'.csv'  # Example file path
        # Open the file in binary mode
        with codecs.open(file_path, 'rb', encoding='utf-8-sig') as f:
            response = HttpResponse(f.read(), content_type='text/csv', charset='utf-8-sig')
            # Set the Content-Disposition header to force download
            name = 'attachment;filename="'+course.course_name+'.csv"'
            response['Content-Disposition'] = name
            return response
    else :
        return render(request, 'main/error.html')
    
@csrf_exempt
def sign_in(request):
    print("in")
    data = request.POST
    course_id = int(data['class'])
    student_profile = get_object_or_404(UserProfile, student_id=data['name'])
    student = student_profile.user
    student_id = student.id
    course = get_object_or_404(Course, id=course_id)
    print('student:', student_profile.student_id, 'sign in', course.course_name)
    if course.students.filter(id = student_id).count() > 0:
        error_code, date, time_interval = check_time(course.start_date)
        print('date =', date)
        date = '6/1'
        path = './csvfile/'+str(course.id)+'.csv'
        print(path, student_profile.student_id, date)
        error_code = One_Student_Sign(path, student_profile.student_id, date)
    return 0

def save_file(csv_file, path):
    with open(path, 'wb+') as destination:
        for chunk in csv_file.chunks():
            destination.write(chunk)

def delete_file(path):
    if os.path.exists(path):
        os.remove(path)

def signin_list(request):
    course_list = Course.objects.all()
    context = {
            'course_list': course_list,
            'profile' : profile
        }
    return render(request, 'main/sign_list.html', context)

#change
def home(request):
    course_id = request.POST.get("course_id")
    course_name = request.POST.get("course_name")
    course_list = Course.objects.all()
    error = False
    if course_id != None and course_id != '' and course_name != None and course_name != '':
        course_id = int(course_id)
        if Course.objects.filter(id = course_id, course_name = course_name).count() > 0:
            course_list = Course.objects.filter(id = course_id, course_name = course_name)
        else : error = True
    elif course_id != None and course_id != '' : 
        course_id = int(course_id)
        if Course.objects.filter(id = course_id).count() > 0:
            course_list = Course.objects.filter(id = course_id)
        else : error = True
    elif course_name != None and course_name != '' :
        if Course.objects.filter(course_name = course_name).count() > 0:
            course_list = Course.objects.filter(course_name = course_name)
        else : error = True

    if request.user.is_authenticated:
        profile = get_object_or_404(UserProfile, user=request.user)
        context = {
            'error' : error,
            'course_list': course_list,
            'profile' : profile
        }
        print("user is", request.user)
    else:
        context = {
            'error' : error,
            'course_list': course_list
        }
    return render(request, 'main/home.html', context)

def parse_time(time_now):
    for i in range(len(index_list)):
        start_time = datetime.datetime(time_now.year, time_now.month, time_now.day, course_time_list[i][0], course_time_list[i][1], 0, 0)
        end_time = datetime.datetime(time_now.year, time_now.month, time_now.day, course_time_list[i][2], course_time_list[i][3], 0, 0)
        if time_now >= start_time and time_now <= end_time:
            return index_list[i]
    
    return -1

def check_time(course_time):#格式週一 : 1 2 3, 週二 : 1 2 3
    time_now = datetime.datetime.now()
    weekday_now = datetime.date.today().weekday()
    time_interval = parse_time(time_now)
    course_time = course_time.split(',')
    for day in course_time:
        day_split = day.split(':')
        date = day_split[0].strip()
        time = day_split[1].split()
        if week_list[weekday_now] == date and time_interval in time:
            return 'true', str(time_now.month)+'/'+str(time_now.day), time_interval
         
    return '並不在上課期間，無法簽到', '0/0', -1
    
@login_required
def create_course(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    error_code = 0
    if profile.is_teacher:
        if request.method == 'POST':
            form = Create_course_Form(request.POST, request.FILES)
            if form.is_valid():
                course_name = form.cleaned_data['course_name']
                course_time = form.cleaned_data['course_time']
                course_dest = form.cleaned_data['course_dest']
                course = Course.objects.create(course_name = course_name, start_date = course_time, course_address = course_dest)
                csv_file = form.cleaned_data['csv_file']
                file_path = './csvfile/'+str(course.id)+'.csv'
                save_file(csv_file, file_path)
                error_code = Check_file(file_path)
                if error_code == 'Pass':
                    course.teacher.add(request.user)
                    ID_list = All_students(file_path)
                    for ID in ID_list:
                        if UserProfile.objects.filter(student_id = ID).exists():
                            student = UserProfile.objects.get(student_id = ID)
                            course.students.add(student.user)
                        else:
                            error_code = 2
                            render(request, 'main/create.html', {'form': form, 'user': request.user, 'error' : error_code})
                    
                    form = Create_course_Form()
                    error_code = 1
                    return render(request, 'main/create.html', {'form': form, 'user': request.user, 'error' : error_code})
                else:
                    delete_file(file_path)
                    course.delete()
                    error_code = 3
                    render(request, 'main/create.html', {'form': form, 'user': request.user, 'error' : error_code})
        else:
            form = Create_course_Form()
        
        return render(request, 'main/create.html', {'form': form, 'user': request.user, 'error' : error_code})
    else:
        form = Create_course_Form()
        return render(request, 'main/error.html')
    
@login_required
def history_divide(request, id):
    profile = get_object_or_404(UserProfile, user=request.user)
    if profile.is_teacher:
        course = get_object_or_404(Course, id = id)
        students_list = course.students.all()
        teschers_list = course.teacher.all()
        output_list = []
        for s in students_list:
            url = reverse("main:history", kwargs={"course_id": id, "student_id": s.id})
            stu_profile = get_object_or_404(UserProfile, user=s)
            output_list.append({'student' : s, 'stu_profile' : stu_profile, 'hist_url' : url})
        context = {
            'course' : course,  
            'output_list' : output_list,
            'user': request.user,
            'teachers' : teschers_list
        }
        return render(request, 'main/hist_stu_list.html', context)
    else :
        return redirect(reverse("main:history", kwargs={"course_id": id, "student_id": request.user.id}))

@login_required 
def history(request, course_id, student_id):
    profile = get_object_or_404(UserProfile, user=request.user)
    tag = 0
    if request.user.id == student_id and profile.is_student:
        student = get_object_or_404(User, id = student_id)
        if student.students.filter(id = course_id).count() > 0:
            tag = 1
        elif student.students.filter(id = course_id).count() <= 0:
            tag = 2
    elif profile.is_teacher:
        student = get_object_or_404(User, id = student_id)
        teacher = request.user
        if teacher.teachers.filter(id = course_id).count() > 0 and student.students.filter(id = course_id).count() > 0:
            tag = 1
        elif student.students.filter(id = course_id).count() <= 0:
            tag = 2
        elif teacher.teachers.filter(id = course_id).count() <= 0:
            tag = 3

    if tag == 0:
        render(request, 'main/error.html')
    elif tag == 1:
        course = get_object_or_404(Course, id = course_id)
        student = get_object_or_404(User, id = student_id)
        student_profile = get_object_or_404(UserProfile, user=student)
        file_path = './csvfile/'+str(course_id)+'.csv'
        time_list, signin_list = Search_one_Student(file_path, student_profile.student_id)
        final_list = []
        for i in range(len(time_list)):
            if signin_list[i] :
                final_list.append({'date' : time_list[i], 'sign' : '簽到'})
            else :
                final_list.append({'date' : time_list[i], 'sign' : '未簽到'})

        context = {
            'course' : course,   
            'student' : student,
            'student_profile' : student_profile,
            'final_list' : final_list,
            'user': request.user
        }
        return render(request, 'main/history.html', context)
    elif tag == 2:
        return render(request, 'main/error.html')
    else:
        return render(request, 'main/error.html')

@login_required
def profile(request, id):
    User_profile = get_object_or_404(UserProfile, user=request.user)
    if User_profile.id == id:
        if User_profile.is_teacher:
            course_list = request.user.teachers.all()
        else :
            course_list = request.user.students.all()
        context = {
            'form1' : request.user,
            'form2' : User_profile,
            'course_list' : course_list,
            'form3' : User_profile
        }
        return render(request, 'main/profile.html', context)
    else:
        Requested_profile = get_object_or_404(UserProfile, id = id)
        if Requested_profile.is_teacher:
            course_list = Requested_profile.user.teachers.all()
            context = {
                'form1' : Requested_profile.user,
                'form2' : Requested_profile,
                'course_list' : course_list,
                'form3' : User_profile
            }
            return render(request, 'main/profile.html', context)
        elif User_profile.is_teacher:
            if Requested_profile.is_teacher:
                course_list = Requested_profile.user.teachers.all()
            else :
                course_list = Requested_profile.user.students.all()
            context = {
                'form1' : Requested_profile.user,
                'form2' : Requested_profile,
                'course_list' : course_list,
                'form3' : User_profile
            }
            return render(request, 'main/profile.html', context)
        else:
            return render(request, 'main/error.html')

def log_in(request):
    form = LoginForm()
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            profile = get_object_or_404(UserProfile, user=user)
            return redirect(reverse("main:profile", kwargs={"id": profile.id}))  #重新導向到首頁
    context = {
        'form': form
    }
    return render(request, 'main/login.html', context)
   
def course_profile(request, id):
    course = get_object_or_404(Course, id = id)
    students_list = course.students.all()
    teachers_list = course.teacher.all()

    students = []
    teachers = []
    for s in students_list:
        profile = get_object_or_404(UserProfile, user = s)
        students.append({'User' : s, 'Profile' : profile})
    for t in teachers_list:
        profile = get_object_or_404(UserProfile, user = t)
        teachers.append({'User' : t, 'Profile' : profile})
    context = {
        'course' : course,
        'teachers' : teachers,
        'students' : students,
        'user': request.user
    }
    return render(request, "main/course_profile.html", context)

def log_out(request):
    logout(request)
    return redirect(reverse("main:home"))
        
def test_list(request):
    time_list = [{'date' : '5/12', 'sign' : True}, {'date' : '5/13', 'sign' : False}]
    context = {
        'time_list': time_list
    }
    return render(request, 'main/test_list.html', context)

def registration(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("main:login"))

    context = {
        'form': form
    }
    return render(request, 'main/registration.html', context)     
