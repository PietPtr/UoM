from django.urls import path

from . import views

urlpatterns = [
    path('course/<int:course_id>/enroll',
         views.enroll_in_course, name='enroll_in_course'),
    path('course/<int:course_id>/', views.view_course, name='view_course'),
    path('', views.all_courses, name='all_courses'),
]
