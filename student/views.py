from django.shortcuts import render, get_object_or_404

from teacher.models import *


def all_courses(request):
    context = {
        'courses': Course.objects.filter(published=True)
    }
    return render(request, 'all_courses.html', context)


def view_course(request, course_id):
    context = {
        'course': get_object_or_404(Course, pk=course_id),
        'aims': Aim.objects.filter(course_id=course_id)
    }

    return render(request, 'course.html', context)
