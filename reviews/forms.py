from django import forms
from django.core.exceptions import ValidationError

from reviews.models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['user', 'course', 'text', 'rating']

    def clean_text(self):
        text = self.cleaned_data['text'].strip()
        if len(text) > 1000:
            raise ValidationError("Текст должен содержать не более 1000 символов")
        return text

    def clean_rating(self):
        rating = self.cleaned_data['rating']
        if not 1 <= rating <= 10 and not type(rating) is int:
            raise ValidationError("Рейтинг должен быть от 1 до 10")
        return rating
