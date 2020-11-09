from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.db.models import Max

from teacher.models import Course, Aim, Action
from teacher.forms import *

import json


def new_aim(request, course_id):
    if request.method == 'POST':
        form = NewAimForm(request.POST)
        if form.is_valid():
            aim = Aim(
                description=form.cleaned_data['description'],
                course=Course.objects.get(id=course_id))
            aim.save()
        return redirect('/teacher/course/%s/aims' % course_id)
    else:
        form = NewAimForm()

    context = {
        'form': form,
        'message': 'Enter a new aim for this course.',
        'action_link': '/teacher/new_aim/' + str(course_id) + '/'
    }

    return render(request, 'new_unit.html', context)


def edit_aim(request, aim_id):
    aim = Aim.objects.get(id=aim_id)
    if request.method == 'POST':
        form = NewAimForm(request.POST)
        if form.is_valid():
            aim.description = form.cleaned_data['description']
            aim.save()
        return redirect('/teacher/course/%s/aims' % course_id)
    else:
        form = NewAimForm(initial={
            'description': aim.description
        })

    context = {
        'form': form,
        'message': 'Edit properties of this aim.',
        'action_link': '/teacher/aim/' + str(aim_id) + '/'
    }

    return render(request, 'new_unit.html', context)


def delete_aim(request, aim_id):
    aim = get_object_or_404(Aim, pk=aim_id)

    if request.method == 'POST':
        aim.delete()

    return redirect('/teacher/course/%s/aims' % aim.course.id)
