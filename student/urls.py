from django.urls import path

from . import views

urlpatterns = [
    path('course/<int:course_id>/enroll/confirm',
         views.confirm_enrolment, name="confirm_enrolment"),
    path('course/<int:course_id>/enroll',
         views.enroll_in_course, name='enroll_in_course'),
    path('course/<int:course_id>/', views.view_course, name='view_course'),

    path('course_instance/', views.course_instances, name='course_instances'),
    path('course_instance/<int:instance_id>/',
         views.view_instance, name='view_instance'),
    path('course_instance/<int:instance_id>/materials/',
         views.view_instance_materials, name='view_instance_materials'),
    path('course_instance/<int:instance_id>/aims/',
         views.view_instance_aims, name='view_instance_aims'),
    path('course_instance/<int:instance_id>/actions/',
         views.view_instance_actions, name='view_instance_actions'),

    path('course_instance/<int:instance_id>/action/<int:action_id>',
         views.view_action, name='view_action'),
    path('course_instance/<int:instance_id>/action/<int:action_id>/complete',
         views.complete_action, name='complete_action'),
    path('course_instance/<int:instance_id>/action/<int:action_id>/undo_complete',
         views.undo_complete_action, name='undo_complete_action'),

    path('', views.all_courses, name='all_courses'),
]
