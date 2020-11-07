from django.urls import path

from . import views

urlpatterns = [

    path('', views.all_coursess, name='all_courses'),
]
