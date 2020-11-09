from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.db.models import Max

from teacher.models import Course, Aim, Action
from teacher.forms import *

import json


def new_action(request, course_id):
    if request.method == 'POST':
        form = NewActionForm(request.POST, course_id=course_id)
        if form.is_valid():
            action = Action(
                description=form.cleaned_data['description'],
                course=Course.objects.get(id=course_id),
                load=form.cleaned_data['load'],
                ordering=Action.objects.filter(course_id=course_id).count())

            action.save()
            return redirect('/teacher/course/%s/actions' % course_id)
    else:
        form = NewActionForm(course_id=course_id)

    context = {
        'form': form,
        'message': 'Enter a new learning action for this course.',
        'action_link': '/teacher/new_action/' + str(course_id) + '/'
    }

    return render(request, 'new_unit.html', context)


def edit_action(request, action_id):
    action = get_object_or_404(Action, pk=action_id)
    course_id = action.course.id
    if request.method == 'POST':
        form = NewActionForm(request.POST, course_id=course_id)
        if form.is_valid():
            action.description = form.cleaned_data['description']
            action.aims.set(form.cleaned_data['aims'])
            action.materials.set(form.cleaned_data['materials'])
            action.load = form.cleaned_data['load']
            action.save()
        return redirect('/teacher/course/%s/actions' % course_id)
    else:
        print(action.aims.all())
        form = NewActionForm(initial={
            'description': action.description,
            'aims': action.aims.all(),
            'materials': action.materials.all()
        }, course_id=course_id)

    context = {
        'form': form,
        'message': 'Edit properties of this action.',
        'action_link': '/teacher/action/' + str(action_id) + '/'
    }

    return render(request, 'new_unit.html', context)


def edit_action_order(request, action_id):
    action = get_object_or_404(Action, pk=action_id)
    course = get_object_or_404(Course, pk=action.course_id)

    largest = Action.objects \
        .filter(course_id=course.id) \
        .aggregate(Max('ordering'))['ordering__max']

    print(request)

    if request.method == 'POST':
        direction = request.POST['direction']
        if direction == 'up':
            if action.ordering != 0:
                action_above = Action.objects.get(
                    ordering=(action.ordering - 1))
                action_above.ordering += 1
                action.ordering -= 1
                action.save()
                action_above.save()
        if direction == 'down':
            if action.ordering != largest:
                action_below = Action.objects.get(
                    ordering=(action.ordering + 1))
                action_below.ordering -= 1
                action.ordering += 1
                action.save()
                action_below.save()

    return HttpResponse(json.dumps({}), content_type="application/json")


def delete_action(request, action_id):
    action = get_object_or_404(Action, pk=action_id)

    if request.method == 'POST':
        action.delete()

    return redirect('/teacher/course/%s/actions' % action.course.id)
