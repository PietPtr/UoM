from django import forms

from .models import *


class NewCourseForm(forms.Form):
    course_name = forms.CharField(label='Course name', max_length=256)
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea)
    study_load = forms.IntegerField(label='Study load in hours')


class NewAimForm(forms.Form):
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea)


class NewActionForm(forms.Form):
    description = forms.CharField(
        label='Description',
        widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        course_id = kwargs.pop('course_id')
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['aims'] = forms.ModelMultipleChoiceField(
            Aim.objects.filter(course=course_id),
            widget=forms.CheckboxSelectMultiple)

        self.fields['materials'] = forms.ModelMultipleChoiceField(
            Material.objects.filter(course=course_id),
            widget=forms.CheckboxSelectMultiple)


class NewMaterialForm(forms.Form):
    file = forms.FileField()
