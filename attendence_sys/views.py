from django import views
from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.views import View
from gtts import gTTS
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import Student, Attendence
from .filters import AttendenceFilter
import pyttsx3 as textSpeach

import csv
from .recognizer import Recognizer
from datetime import date


from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

engine = textSpeach.init()
@login_required(login_url='login')
def home(request):
    studentForm = CreateStudentForm()

    if request.method == 'POST':
        studentForm = CreateStudentForm(data=request.POST, files=request.FILES)
        # print(request.POST)
        stat = False
        try:
            student = Student.objects.get(
                registration_id=request.POST['registration_id'])
            stat = True
        except:
            stat = False
        if studentForm.is_valid() and (stat == False):
            studentForm.save()
            name = studentForm.cleaned_data.get(
                'firstname') + " " + studentForm.cleaned_data.get('lastname')
            messages.success(request, 'Student ' + name +
                             ' was successfully added.')
            return redirect('home')
        else:
            messages.error(request, 'Student with Registration Id ' +
                           request.POST['registration_id']+' already exists.')
            return redirect('home')

    context = {'studentForm': studentForm}
    return render(request, 'attendence_sys/home.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or Password is incorrect')
            
    context = {}
    return render(request, 'attendence_sys/login.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def updateStudentRedirect(request):
    context = {}
    if request.method == 'POST':
        try:
            reg_id = request.POST['reg_id']
            branch = request.POST['branch']
            student = Student.objects.get(
                registration_id=reg_id, branch=branch)
            updateStudentForm = CreateStudentForm(instance=student)
            context = {'form': updateStudentForm,
                       'prev_reg_id': reg_id, 'student': student}
        except:
            messages.error(request, 'Student Not Found')
            return redirect('home')
    return render(request, 'attendence_sys/student_update.html', context)


@login_required(login_url='login')
def updateStudent(request):
    if request.method == 'POST':
        context = {}
        try:
            student = Student.objects.get(
                registration_id=request.POST['prev_reg_id'])
            updateStudentForm = CreateStudentForm(
                data=request.POST, files=request.FILES, instance=student)
            if updateStudentForm.is_valid():
                updateStudentForm.save()
                messages.success(request, 'Updation Success')
                
                statment = str('Updation Success')
                engine.say(statment)
                engine.runAndWait()
                
                return redirect('home')
        except:
            messages.error(request, 'Updation Unsucessfull')
            return redirect('home')
    return render(request, 'attendence_sys/student_update.html', context)


@login_required(login_url='login')
def takeAttendence(request):
    if request.method == 'POST':
        details = {
            'branch': request.POST['branch'],
            'year': request.POST['year'],
            'section': request.POST['section'],
            'period': request.POST['period'],
            'faculty': request.user.faculty
        }
        if Attendence.objects.filter(date=str(date.today()), branch=details['branch'], year=details['year'], section=details['section'], period=details['period']).count() != 0:
            messages.error(request, "Attendence already recorded.")
            statment = str('Attendence already recorded')
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)
            engine.say(statment)
            #engine.runAndWait()
            engine.stop()
            return redirect('home')
        else:
            students = Student.objects.filter(
                branch=details['branch'], year=details['year'], section=details['section'])
            names = Recognizer(details)
            for student in students:
                if str(student.registration_id) in names:
                    attendence = Attendence(Faculty_Name=request.user.faculty,
                                            Student_ID=str(
                                                student.registration_id),
                                            period=details['period'],
                                            branch=details['branch'],
                                            year=details['year'],
                                            section=details['section'],
                                            status='Present')
                    attendence.save()
                    voices = engine.getProperty('voices')
                    engine.setProperty('voice', voices[1].id)
                    statment = str('attendence saved Thank You')
                    engine.say(statment)
                    engine.runAndWait()
                else:
                    attendence = Attendence(Faculty_Name=request.user.faculty,
                                            Student_ID=str(
                                                student.registration_id),
                                            period=details['period'],
                                            branch=details['branch'],
                                            year=details['year'],
                                            section=details['section'])
                    attendence.save()
            attendences = Attendence.objects.filter(date=str(date.today()), branch=details['branch'], year=details['year'], section=details['section'], period=details['period'])
            context = {"attendences": attendences, "ta": True}
            messages.success(request, "Attendence taking Success")
            
            return render(request, 'attendence_sys/attendence.html', context)
    context = {}
    return render(request, 'attendence_sys/home.html', context)

def searchAttendence(request):
    attendences = Attendence.objects.all()
    myFilter = AttendenceFilter(request.GET, queryset=attendences)
    attendences = myFilter.qs
    context = {'myFilter': myFilter, 'attendences': attendences, 'ta': False}
    return render(request, 'attendence_sys/attendence.html', context)


def facultyProfile(request):
    faculty = request.user.faculty
    form = FacultyForm(instance=faculty)
    context = {'form': form}
    return render(request, 'attendence_sys/facultyForm.html', context)

def venue_pdf(request):
    	# Create Bytestream buffer
	buf = io.BytesIO()
	# Create a canvas
	c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
	# Create a text object
	textob = c.beginText()
	textob.setTextOrigin(inch, inch)
	textob.setFont("Helvetica", 14)

	# Add some lines of text
	lines = [
		"This is line 1",
		"This is line 2",
		"This is line 3",
	    ]
	# Loop
	for line in lines:
		textob.textLine(line)

	# Finish Up
	c.drawText(textob)
	c.showPage()
	c.save()
	buf.seek(0)

	# Return something
	return FileResponse(buf, as_attachment=True, filename='Attendence.pdf')


def venue_csv(request):
  
    response=HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=csv' + '.csv'

    writer =csv.writer(response)
    writer.writerow(['DATE ','YEAR','SECTION','PERIOD','BRANCH','NAME'])
    #branch = request.POST['branch']
    
    attendences = Attendence.objects.all()
    myFilter = AttendenceFilter(request.GET, queryset=attendences)
    attendences = myFilter.qs
    writer.writerow(attendences)
    
    return response

