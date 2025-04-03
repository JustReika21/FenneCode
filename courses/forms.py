from django import forms


class EnrollmentForm(forms.Form):
    user = forms.IntegerField(widget=forms.HiddenInput)
    course = forms.IntegerField(widget=forms.HiddenInput)


class CourseReviewForm(forms.Form):
    user = forms.IntegerField(widget=forms.HiddenInput)
    course = forms.IntegerField(widget=forms.HiddenInput)
    text = forms.CharField(max_length=1024)
    rating = forms.ChoiceField(choices=[i for i in range(1, 11)])
