from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.db.models import Max

from teacher.models import Course, Aim, Action
from teacher.forms import *

import json


def all_courses(request):
    context = {
        'courses': Course.objects.all()
    }
    return render(request, 'overview.html', context)


def new_course(request):
    if request.method == 'POST':
        form = NewCourseForm(request.POST)
        if form.is_valid():
            course = Course(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                published=form.cleaned_data['published']
            )
            course.save()
            return view_course(request, course.id)
    else:
        form = NewCourseForm()

    context = {
        'form': form,
        'message': 'Enter a name for this course.',
        'action_link': '/teacher/new_course/'
    }

    return render(request, 'new_unit.html', context)


def view_course(request, course_id):
    context = {
        'course': get_object_or_404(Course, pk=course_id),
        'study_load': sum([action.load for action in Action.objects.filter(course=course_id)]),
        'nav': 'home'
    }

    return render(request, 'course/course.html', context)


def view_course_aims(request, course_id):
    context = {
        'course': get_object_or_404(Course, pk=course_id),
        'aims': Aim.objects.filter(course=course_id),
        'nav': 'aims'
    }

    return render(request, 'course/aims.html', context)


def view_course_actions(request, course_id):
    context = {
        'course': get_object_or_404(Course, pk=course_id),
        'actions': Action.objects.filter(course=course_id).order_by('ordering'),
        'nav': 'actions'
    }

    return render(request, 'course/actions.html', context)


def view_course_materials(request, course_id):
    context = {
        'course': get_object_or_404(Course, pk=course_id),
        'materials': Material.objects.filter(course=course_id),
        'nav': 'materials'
    }

    return render(request, 'course/materials.html', context)


def edit_course_details(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.method == 'POST':
        form = NewCourseForm(request.POST)
        if form.is_valid():
            course.name = form.cleaned_data['name']
            course.description = form.cleaned_data['description']
            course.published = form.cleaned_data['published']
            course.save()
        return redirect('/teacher/course/%s' % course_id)
    else:
        form = NewCourseForm(initial={
            'name': course.name,
            'description': course.description,
            'published': course.published
        })

    context = {
        'form': form,
        'message': 'Edit course name and description.',
        'action_link': '/teacher/course/%s/details/' % course.id
    }

    return render(request, 'new_unit.html', context)


def delete_course(request, course_id):
    pass
