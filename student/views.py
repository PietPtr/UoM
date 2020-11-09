from django.shortcuts import render

from teacher.models import *


def all_courses(request):
    context = {
        'courses': Course.objects.filter(published=True)
    }
    return render(request, 'all_courses.html', context)


def view_course(request, course_id):

    return render(request, 'course.html', {})
