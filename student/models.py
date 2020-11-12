from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from teacher.models import *


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return 'Student %s' % self.user.username


class CourseInstance(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    completed_actions = models.ManyToManyField(Action)
    started = models.DateField(auto_now=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return '\'%s\' %s-%s (%s)' % \
            (self.course.name,
             self.started.month,
             self.started.year,
             self.student.user.username)


@receiver(post_save, sender=User)
def create_user_student(sender, instance, created, **kwargs):
    if created:
        Student.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_student(sender, instance, **kwargs):
    instance.student.save()
