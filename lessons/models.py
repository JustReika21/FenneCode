from django.db import models

from courses.models import Course
from fennecode import settings


class Lesson(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    position = models.PositiveSmallIntegerField(default=1)
    total_points = models.PositiveSmallIntegerField(default=0)
    user_lesson_complete = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='user_lesson_complete',
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['course', 'position'],
                name='unique_lesson_position'
            )
        ]
