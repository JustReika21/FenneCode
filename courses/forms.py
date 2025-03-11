from django import forms


class EnrollmentForm(forms.Form):
    user = forms.IntegerField(widget=forms.HiddenInput)
    course = forms.IntegerField(widget=forms.HiddenInput)
