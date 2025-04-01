from django import forms


class SubmitMultipleChoiceTaskAnswerForm(forms.Form):
    user = forms.IntegerField(widget=forms.HiddenInput())
    choice_task = forms.IntegerField(widget=forms.HiddenInput())
    selected_answers = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
