from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.db.models import Max, Min

from teacher.models import Course, Aim, Action
from teacher.forms import *

import json


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


def edit_action_order(request, action_id):
    action = get_object_or_404(Action, pk=action_id)
    course = get_object_or_404(Course, pk=action.course_id)

    largest = Action.objects \
        .filter(course_id=course.id) \
        .aggregate(Max('ordering'))['ordering__max']

    if request.method == 'POST':
        direction = request.POST['direction']
        if direction == 'up':

            if action.ordering != 0:
                smallest_in_week = Action.objects.filter(
                    week=action.week.id).aggregate(Min('ordering'))['ordering__min']

                if action.ordering != smallest_in_week:
                    action_above = Action.objects.get(
                        course_id=course.id,
                        ordering=(action.ordering - 1))

                    switch_actions(action_above, action)
                else:
                    previous_week = get_object_or_404(
                        Week, course=course.id, number=(action.week.number - 1))
                    action.week = previous_week
                    action.save()

        if direction == 'down':
            largest_in_week = Action.objects.filter(
                week=action.week.id).aggregate(Max('ordering'))['ordering__max']

            if action.ordering != largest_in_week:
                action_below = Action.objects.get(
                    course_id=course.id,
                    ordering=(action.ordering + 1))

                switch_actions(action, action_below)
            elif action.week.number != action.course.weeks:
                next_week = get_object_or_404(Week,
                                              course=course.id, number=(action.week.number + 1))
                action.week = next_week
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

    if request.method == 'POST':
        week.delete()

    later_weeks = Week.objects.filter(number__gt=week.number)

    print(later_weeks)

    for week in later_weeks:
        week.number -= 1
        week.save()

    return redirect('/teacher/course/%s/actions' % week.course.id)
