from django.urls import path

from . import views

urlpatterns = [
    path('course/<int:course_id>/', views.view_course, name="view_course_details"),
    path('course/<int:course_id>/aims',
         views.view_course_aims, name="view_course_aims"),
    path('course/<int:course_id>/actions',
         views.view_course_actions, name="view_course_actions"),
    path('course/<int:course_id>/materials',
         views.view_course_materials, name="view_course_materials"),

    path('course/<int:course_id>/details/',
         views.edit_course_details, name="edit_course_details"),
    path('aim/<int:aim_id>/', views.edit_aim, name="edit_aim"),
    path('action/<int:action_id>/', views.edit_action, name="edit_action"),
    path('action/<int:action_id>/ordering/',
         views.edit_action_order, name="edit_action_order"),

    path('new_aim/<int:course_id>/', views.new_aim, name="new_aim"),
    path('new_action/<int:course_id>/', views.new_action, name="new_action"),
    path('new_material/<int:course_id>/',
         views.new_material, name="new_material"),
    path('new_course/', views.new_course, name='new_course'),

    path('add_week/<int:course_id>/', views.add_week, name='add_week'),

    path('', views.all_courses, name='my_courses'),
    path('delete_aim/<int:aim_id>/', views.delete_aim, name='delete_aim'),
    path('delete_action/<int:action_id>/',
         views.delete_action, name='delete_action'),
    path('delete_material/<int:material_id>/',
         views.delete_material, name='delete_material'),
    path('delete_week/<int:week_id>/', views.delete_week, name='delete_week')
]
