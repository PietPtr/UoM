from django.urls import path

from . import views

urlpatterns = [
    path('course/<int:course_id>/', views.view_course, name='view_course'),
    path('', views.all_courses, name='all_courses'),
]
