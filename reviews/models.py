from django.db import models

from courses.models import Course
from fennecode import settings


class Review(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(blank=True)
    rating = models.SmallIntegerField(
        default=0,
        choices=[(i, i) for i in range(1, 11)],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} {self.course} ({self.rating}/10)'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'course'],
                name='unique_review'
            ),
        ]
