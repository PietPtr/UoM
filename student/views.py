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
