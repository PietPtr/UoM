from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic

from .models import Course, Aim, Action
from .forms import *


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
                name=form.cleaned_data['course_name'],
                description=form.cleaned_data['description'],
                study_load=form.cleaned_data['study_load']
            )
            course.save()
            return edit_course(request, course.id)
    else:
        form = NewCourseForm()

    context = {
        'form': form,
        'message': 'Enter a name for this course.',
        'action_link': '/teacher/new_course/'
    }

    return render(request, 'new_unit.html', context)


def edit_course(request, course_id):
    context = {}
    context['course'] = Course.objects.get(pk=course_id)
    context['aims'] = Aim.objects.filter(course=course_id)
    context['actions'] = Action.objects.filter(course=course_id)
    context['materials'] = Material.objects.filter(course=course_id)

    return render(request, 'course.html', context)


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
        return edit_course(request, course_id)
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
        return edit_course(request, aim.course.id)
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

    return edit_course(request, aim.course.id)


def new_action(request, course_id):
    if request.method == 'POST':
        form = NewActionForm(request.POST, course_id=course_id)
        if form.is_valid():
            action = Action(
                description=form.cleaned_data['description'],
                course=Course.objects.get(id=course_id))
            # TODO: file connectie
            action.save()
            return edit_course(request, course_id)
    else:
        form = NewActionForm(course_id=course_id)

    context = {
        'form': form,
        'message': 'Enter a new learning action for this course.',
        'action_link': '/teacher/new_action/' + str(course_id) + '/'
    }

    return render(request, 'new_unit.html', context)


def edit_action(request, action_id):
    action = Action.objects.get(id=action_id)
    course_id = action.course.id
    if request.method == 'POST':
        form = NewActionForm(request.POST, course_id=course_id)
        if form.is_valid():
            action.description = form.cleaned_data['description']
            action.aims.set(form.cleaned_data['aims'])
            action.save()
        return edit_course(request, course_id)
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


def delete_action(request, action_id):
    action = get_object_or_404(Action, pk=action_id)

    if request.method == 'POST':
        action.delete()

    return edit_course(request, action.course.id)


def new_material(request, course_id):
    if request.method == 'POST':
        form = NewMaterialForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.FILES)
            material = Material(
                file=request.FILES['file'],
                course=Course.objects.get(id=course_id))
            material.save()
            return edit_course(request, course_id)
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

    return edit_course(request, material.course.id)
