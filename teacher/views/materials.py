from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.db.models import Max

from teacher.models import Course, Aim, Action
from teacher.forms import *

import json


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
