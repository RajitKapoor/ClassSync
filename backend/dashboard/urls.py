"""
URLs for dashboard app.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('student/', views.student_dashboard, name='student-dashboard'),
    path('teacher/', views.teacher_dashboard, name='teacher-dashboard'),
    path('admin/', views.admin_dashboard, name='admin-dashboard'),
]

