from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Course)
admin.site.register(Aim)
admin.site.register(Action)
admin.site.register(Material)
