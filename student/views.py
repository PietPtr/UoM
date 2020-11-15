from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

from teacher.models import *
from student.models import *

from datetime import date, datetime, timedelta
from icalendar import Calendar, Event

import json
import copy

from pprint import pprint
from random import randint


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

    return redirect('/student/course_instance/%s/' % course_instance.id)


def course_instances(request):
    context = {
        'instances': CourseInstance.objects.filter(student=request.user.student).order_by('-started')
    }

    return render(request, 'course_instances.html', context)


def view_instance(request, instance_id):
    context = {
        'instance': get_object_or_404(CourseInstance, pk=instance_id),
        'nav': 'home'
    }

    return render(request, 'instance/home.html', context)


def view_instance_aims(request, instance_id):
    instance = get_object_or_404(CourseInstance, pk=instance_id)
    context = {
        'instance': instance,
        'aims': Aim.objects.filter(course=instance.course.id),
        'nav': 'aims'
    }

    return render(request, 'instance/aims.html', context)


def view_instance_actions(request, instance_id):
    instance = get_object_or_404(CourseInstance, pk=instance_id)
    course = instance.course
    weeks = Week.objects.filter(course=course.id).order_by('number')

    completed_actions = instance.completed_actions.all()

    rows = []

    for week in weeks:
        actions = Action.objects.filter(
            week=week.id, course=course.id).order_by('ordering')

        row = {
            'type': 'week',
            'description': 'Week %s' % week.number,
            'id': week.id,
            'green': all(action in completed_actions for action in actions) and len(actions) != 0
        }

        rows.append(row)

        for action in actions:
            row = {
                'type': 'action',
                'description': action.description,
                'load': action.load,
                'id': action.id,
                'ordering': action.ordering,
                'green': action in completed_actions
            }
            rows.append(row)

    context = {
        'instance': get_object_or_404(CourseInstance, pk=instance_id),
        'actions': Action.objects.filter(course=course.id).order_by('ordering'),
        'rows': rows,
        'nav': 'actions'
    }

    return render(request, 'instance/actions.html', context)


def view_instance_materials(request, instance_id):
    instance = get_object_or_404(CourseInstance, pk=instance_id)
    course = instance.course
    context = {
        'instance': instance,
        'materials': Material.objects.filter(course=course.id),
        'nav': 'materials'
    }

    return render(request, 'instance/materials.html', context)


def view_action(request, instance_id, action_id):
    instance = get_object_or_404(CourseInstance, pk=instance_id)
    action = get_object_or_404(Action, pk=action_id)
    materials = action.materials.all()

    context = {
        'instance': instance,
        'action': action,
        'materials': materials,
        'completed': instance.completed_actions.filter(pk=action.id).first()
    }

    return render(request, 'instance/action.html', context)


def complete_action(request, instance_id, action_id):
    instance = get_object_or_404(CourseInstance, pk=instance_id)
    action = get_object_or_404(Action, pk=action_id)

    instance.completed_actions.add(action)

    return view_instance_actions(request, instance_id)


def undo_complete_action(request, instance_id, action_id):
    instance = get_object_or_404(CourseInstance, pk=instance_id)
    action = get_object_or_404(Action, pk=action_id)

    instance.completed_actions.remove(action)

    return view_instance_actions(request, instance_id)


def view_planner(request, instance_id):
    instance = get_object_or_404(CourseInstance, pk=instance_id)

    context = {
        'instance': instance,
        'nav': 'planner',
        'maxload': instance.course.biggest_week_load(),
        'weeks': instance.course.largest_week_number(),
        'today': date.today().strftime('%Y-%m-%d')
    }

    return render(request, 'instance/planner.html', context)


def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0:
        days_ahead += 7
    return d + timedelta(days_ahead)


def divide_load(block_size, load):
    study_blocks = []
    while load > 0:
        this_block_size = block_size if block_size < load else load
        study_blocks.append(this_block_size)
        load -= this_block_size

    return study_blocks


def date_to_datetime(date):
    return datetime(date.year, date.month, date.day)


def to_date(monday, blocktime):
    diff = blocktime - datetime(1970, 1, 1, 0)
    return date_to_datetime(monday) + diff


"""
Planner v2.0 use `django-cal` to publish the ICS as a feed, this way calendar apps can
subscribe to the feed. This means that per course instance a timetable will be saved, so the
users free time settings should also be saved. Problem: users cannot easily change times in their
calendars...
"""


def generate_ics(request, instance_id):
    if request.method == 'POST':
        instance = get_object_or_404(CourseInstance, pk=instance_id)

        blocks = json.loads(request.POST['blocks'])
        max_block_size = int(request.POST['maxBlockSize'])
        try:
            skipped_weeks = [int(x)
                             for x in request.POST['skippedWeeks'].split(',')]
        except ValueError:
            skipped_weeks = []
        min_time_between = int(request.POST['minTimeBetween'])

        dt_blocks = []
        for [[startday, starthour], [endday, endhour]] in blocks:
            startday += 1
            endday += 1

            start = datetime(1970, 1, startday, starthour)
            end = datetime(1970, 1, endday, endhour)

            dt_blocks.append((start, end))

        cal = Calendar()
        cal.add('prodid', '-//UoM//uhm.nl//')
        cal.add('version', '1.0')

        weeks = Week.objects.filter(course_id=instance.course.id)
        actions = Action.objects.filter(
            course_id=instance.course.id).order_by('ordering')

        week_number = 1
        monday = next_weekday(instance.started, 0)
        current_week_free = dt_blocks.copy()

        final_study_blocks = []

        last_next_block_min_bound = None
        for action in actions:
            if action.week.number < week_number:
                continue
            if action.week.number > week_number:
                diff = action.week.number - week_number
                week_number += diff
                current_week_free = dt_blocks.copy()
                last_next_block_min_bound = None
                while diff > 0:
                    monday = next_weekday(monday, 0)

                    iso_week_number = monday.isocalendar()[1]

                    if iso_week_number not in skipped_weeks:
                        diff -= 1

            study_blocks = [action.load]
            if (action.splittable):
                study_blocks = divide_load(max_block_size, action.load)

            for study_block in study_blocks:
                scheduled = False
                for i in range(len(current_week_free)):
                    (start, end) = current_week_free[i]
                    if (last_next_block_min_bound != None):
                        if (last_next_block_min_bound < end and last_next_block_min_bound >= start):
                            start = last_next_block_min_bound
                        elif (last_next_block_min_bound > end):
                            continue  # The next study block should be in the next timeslot

                    block_length = (end - start).seconds // 3600
                    if study_block > block_length:
                        # This free time block is not large enough for the
                        # planned study block
                        continue

                    study_block_end_time = start + timedelta(hours=study_block)
                    next_block_min_bound = study_block_end_time + \
                        timedelta(hours=min_time_between)

                    final_block = (action.description,
                                   to_date(monday, start),
                                   to_date(monday, study_block_end_time))
                    final_study_blocks.append(final_block)

                    current_week_free[i] = (
                        start + timedelta(seconds=study_block*3600), end)

                    last_next_block_min_bound = next_block_min_bound

                    if (i > 0):
                        del current_week_free[0:i-1]

                    scheduled = True
                    break
                if not scheduled:
                    # TODO: Communicate this to the user
                    print("Could not schedule study block of %s hours for '%s'" % (
                        study_block, action))

        for (descr, start, end) in final_study_blocks:
            event = Event()
            event.add('summary', descr)
            event.add('dtstart', start)
            event.add('dtend', end)
            event.add('status', 'CONFIRMED')

            cal.add_component(event)

        return HttpResponse(cal.to_ical(), content_type="text/calendar")
    return HttpResponse('', content_type="text/calendar", status=400)
