from django.urls import path

from . import views

urlpatterns = [
    path('course/<int:course_id>/enroll/confirm',
         views.confirm_enrolment, name="confirm_enrolment"),
    path('course/<int:course_id>/enroll',
         views.enroll_in_course, name='enroll_in_course'),
    path('course/<int:course_id>/', views.view_course, name='view_course'),

    path('course_instance/', views.course_instances, name='course_instances'),

    path('', views.all_courses, name='all_courses'),
]
