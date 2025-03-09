from django import forms

from courses.models import Enrollment


class EnrollmentForm(forms.Form):
    user = forms.IntegerField(widget=forms.HiddenInput)
    course = forms.IntegerField(widget=forms.HiddenInput)
