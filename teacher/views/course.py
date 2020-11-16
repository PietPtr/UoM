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

            week = Week(number=1, course=course)
            week.save()

            return view_course(request, course.id)
    else:
        form = NewCourseForm()

    context = {
        'form': form,
        'message': 'Enter a name for this course.',
        'action_link': reverse('new_course')
    }

    return render(request, 'new_unit.html', context)


def view_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    context = {
        'course': course,
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
    weeks = Week.objects.filter(course=course_id).order_by('number')

    rows = []

    for week in weeks:

        row = {
            'type': 'week',
            'description': 'Week %s' % week.number,
            'id': week.id
        }

        rows.append(row)

        actions = Action.objects.filter(
            week=week.id, course=course_id).order_by('ordering')

        for action in actions:
            row = {
                'type': 'action',
                'description': action.description,
                'load': action.load,
                'id': action.id,
                'ordering': action.ordering
            }
            rows.append(row)

    context = {
        'course': get_object_or_404(Course, pk=course_id),
        'actions': Action.objects.filter(course=course_id).order_by('ordering'),
        'rows': rows,
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
        return redirect(reverse('view_course_details', course_id))
    else:
        form = NewCourseForm(initial={
            'name': course.name,
            'description': course.description,
            'published': course.published
        })

    context = {
        'form': form,
        'message': 'Edit course name and description.',
        'action_link': reverse('edit_course_details', args=[course.id])
    }

    return render(request, 'new_unit.html', context)


def delete_course(request, course_id):
    pass
