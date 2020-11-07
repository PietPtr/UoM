from django.db import models

from teacher.models import *


class CourseInstance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_actions = models.ManyToManyField(Action)


class Student(models.Model):
    enrolled_courses = models.ManyToManyField(CourseInstance)
