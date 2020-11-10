from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.db.models import Max, Min

from teacher.models import Course, Aim, Action
from teacher.forms import *

import json
from pprint import pprint


def new_action(request, course_id):
    if request.method == 'POST':
        form = NewActionForm(request.POST, course_id=course_id)
        if form.is_valid():
            last_week = Week.objects.filter(
                course_id=course_id).order_by('-number').first()

            action = Action.create(
                description=form.cleaned_data['description'],
                course=Course.objects.get(id=course_id),
                load=form.cleaned_data['load'],
                week=last_week)

            action.save()

            action.aims.set(form.cleaned_data['aims'])
            action.materials.set(form.cleaned_data['materials'])

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
            'materials': action.materials.all(),
            'load': action.load
        }, course_id=course_id)

    context = {
        'form': form,
        'message': 'Edit properties of this action.',
        'action_link': '/teacher/action/' + str(action_id) + '/'
    }

    return render(request, 'new_unit.html', context)


def switch_actions(a1, a2):
    a1.ordering += 1
    a2.ordering -= 1
    a1.save()
    a2.save()


def move_action_in_weeks(action, direction):
    mod = 0
    if direction == 'next':
        mod = 1
    elif direction == 'previous':
        mod = -1

    to_week = Week.objects.filter(
        course_id=action.course.id, number=(action.week.number + mod)).first()

    action.week = to_week
    action.save()


def edit_action_order(request, action_id):
    action = get_object_or_404(Action, pk=action_id)
    course = get_object_or_404(Course, pk=action.course_id)

    max_action_ordering = Action.objects \
        .filter(course_id=course.id) \
        .aggregate(Max('ordering'))['ordering__max']

    max_week_number = Week.objects \
        .filter(course_id=course.id) \
        .aggregate(Max('number'))['number__max']

    max_ordering_in_week = Action.objects \
        .filter(course_id=course.id, week_id=action.week.id) \
        .aggregate(Max('ordering'))['ordering__max']

    min_ordering_in_week = Action.objects \
        .filter(course_id=course.id, week_id=action.week.id) \
        .aggregate(Min('ordering'))['ordering__min']

    next_action = Action.objects.filter(
        course_id=course.id, ordering=(action.ordering+1)).first()
    previous_action = Action.objects.filter(
        course_id=course.id, ordering=(action.ordering-1)).first()

    if (request.method == 'POST'):
        direction = request.POST['direction']
        if direction == 'down':
            if action.ordering == max_action_ordering:
                if action.week.number == max_week_number:
                    pass
                else:
                    # move action to next week
                    move_action_in_weeks(action, 'next')
            else:
                if action.ordering == max_ordering_in_week:
                    # move action to next week
                    move_action_in_weeks(action, 'next')
                else:
                    # swap with next action
                    switch_actions(action, next_action)
        elif direction == 'up':
            if action.ordering == 0:
                if action.week.number == 1:
                    pass
                else:
                    # move action to previous week
                    move_action_in_weeks(action, 'previous')
            else:
                if action.ordering == min_ordering_in_week:
                    # mave action to previous week
                    move_action_in_weeks(action, 'previous')
                else:
                    # swap with previous action
                    switch_actions(previous_action, action)

    action.save()

    return HttpResponse(json.dumps({}), content_type="application/json")


def delete_action(request, action_id):
    action = get_object_or_404(Action, pk=action_id)

    if request.method == 'POST':
        action.delete()

    return redirect('/teacher/course/%s/actions' % action.course.id)


def add_week(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    weeks_in_course = Week.objects.filter(course=course).count()

    print(weeks_in_course)

    week = Week(number=weeks_in_course + 1, course=course)
    week.save()

    return HttpResponse(json.dumps({}), content_type="application/json")


def delete_week(request, week_id):
    week = get_object_or_404(Week, pk=week_id)
    course = get_object_or_404(Course, pk=week.course.id)

    if request.method == 'POST':
        if week.number > 1:  # cannot remove the first week, which should always be the last week left
            week.delete()

            later_weeks = Week.objects.filter(number__gt=week.number)

            for week in later_weeks:
                week.number -= 1
                week.save()

    return redirect('/teacher/course/%s/actions' % course.id)
