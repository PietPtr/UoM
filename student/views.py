from django.shortcuts import render, get_object_or_404, redirect

from teacher.models import *
from student.models import *

from datetime import date


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


def enroll_in_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    context = {
        'course': course,
        'already_enrolled': len(CourseInstance.objects.filter(
            student=request.user.student, course=course)) != 0
    }

    return render(request, 'enroll.html', context)


def confirm_enrolment(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course_instance = CourseInstance(
        course=course, student=request.user.student)

    course_instance.save()

    return redirect('/course_instance/%s/' % course_id)


def course_instances(request):
    context = {
        'courses': CourseInstance.objects.filter(student=request.user.student)
    }

    return render(request, 'course_instance.html', context)
