from django.contrib.auth.models import AbstractUser
from django.db import models


class Account(AbstractUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(
        unique=True,
        help_text='Email',
        error_messages={
            'unique': 'Пользователь с такой почтой уже существует.',
            'invalid': 'Почта недействительна',
        }
    )

    # TODO: Phone number verification
    # phone_number = models.CharField(max_length=20, unique=True)

    # TODO: Email verification
    # is_active = models.BooleanField(
    #     default=False,
    # )

    def __str__(self):
        return self.username
