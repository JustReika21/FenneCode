from django.db import models

from fennecode import settings


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='profile',
        on_delete=models.CASCADE
    )
    bio = models.TextField(blank=True)
    telegram = models.CharField(
        max_length=32,
        blank=True,
        help_text="Введите без @",
    )
    avatar = models.ImageField(
        upload_to="user_avatars/",
        default='user_avatars/default.jpg'
    )

    def telegram_link(self):
        if self.telegram:
            return f"https://t.me/{self.telegram}"
        return None

    def __str__(self):
        return self.user.username
