from django.shortcuts import render

from teacher.models import *


def all_coursess(request):
    context = {
        'courses': Course.objects.all()
    }
    return render(request, 'all_courses.html', context)
