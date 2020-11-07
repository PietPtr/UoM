from django.urls import path

from . import views

urlpatterns = [
    path('course/<int:course_id>/', views.edit_course, name="edit_course"),
    path('aim/<int:aim_id>/', views.edit_aim, name="edit_aim"),
    path('action/<int:action_id>/', views.edit_action, name="edit_action"),

    path('new_aim/<int:course_id>/', views.new_aim, name="new_aim"),
    path('new_action/<int:course_id>/', views.new_action, name="new_action"),
    path('new_course/', views.new_course, name='new'),

    path('', views.MyCourses.as_view(), name='my_courses'),
    path('delete_aim/<int:aim_id>/', views.delete_aim, name='delete_aim'),
    path('delete_action/<int:action_id>/',
         views.delete_action, name='delete_action')
]
