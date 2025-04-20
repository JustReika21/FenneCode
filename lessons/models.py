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
    position = models.PositiveSmallIntegerField(default=1)
    total_points = models.PositiveSmallIntegerField(default=0)
    user_lesson_complete = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='user_lesson_complete',
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


class LessonContent(models.Model):
    CONTENT_TYPE = {
        'Text': 'Text',
        'Code': 'Code'
    }
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='content'
    )
    type = models.CharField(max_length=20, choices=CONTENT_TYPE)
    position = models.PositiveSmallIntegerField(default=1)
    content = models.TextField()

    def __str__(self):
        return self.lesson.title
