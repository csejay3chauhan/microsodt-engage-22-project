from django.urls import path
from django.contrib import admin
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('searchattendence/', views.searchAttendence, name='searchattendence'),
    path('account/', views.facultyProfile, name='account'),

    path('updateStudentRedirect/', views.updateStudentRedirect,
         name='updateStudentRedirect'),
    path('updateStudent/', views.updateStudent, name='updateStudent'),
    path('Download/', views.venue_pdf, name='Download'),
    path('csv/', views.venue_csv, name='csv'),
    path('attendence/', views.takeAttendence, name='attendence'),
   
]
