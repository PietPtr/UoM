from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.db.models import Max

from .models import Course, Aim, Action
from .forms import *

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


def new_material(request, course_id):
    if request.method == 'POST':
        form = NewMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = Material(
                file=request.FILES['file'],
                course=Course.objects.get(id=course_id))
            material.save()
            return redirect('/teacher/course/%s/materials' % course_id)
    else:
        form = NewMaterialForm()

    context = {
        'form': form,
        'message': 'Upload new material for this course.',
        'action_link': '/teacher/new_material/' + str(course_id) + '/'
    }

    return render(request, 'new_unit.html', context)


def delete_material(request, material_id):
    material = get_object_or_404(Material, pk=material_id)

    if request.method == 'POST':
        material.delete()

    return redirect('/teacher/course/%s/materials' % material.course.id)
