from django import forms
from django.core.exceptions import ValidationError
from .models import Profile
from django.core.files.images import get_image_dimensions
from PIL import Image
from io import BytesIO
import re


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'telegram', 'avatar']

    def clean_telegram(self):
        telegram = self.cleaned_data['telegram']
        if telegram and not re.match(r'^[a-zA-Z0-9_]{5,32}$', telegram):
            raise ValidationError('Введите действительный телеграм')
        return telegram

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']
        if not avatar:
            return avatar

        if avatar.size > 2 * 1024 * 1024:
            raise ValidationError("Размер аватара не должен превышать 2мб")

        try:
            img = Image.open(avatar)
            img_format = img.format.lower()
            width, height = img.size
            if width < 200 or height < 200:
                raise ValidationError("Разрешение аватара должно быть 200х200")
        except Exception:
            raise ValidationError("Аватар не действителен")

        if img_format not in ['jpeg', 'jpg', 'png']:
            raise ValidationError("Поддерживаются только форматы .jpg, .jpeg и .png")

        return avatar

    def clean_bio(self):
        bio = self.cleaned_data['bio']
        if bio and len(bio) > 200:
            raise ValidationError("Информация о себе не должна превышать 200 символов")
        return bio
