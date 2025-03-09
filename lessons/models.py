from django.contrib.auth import get_user_model
from django.db import models

from courses.models import Course


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=100)
    content = models.TextField()
    position = models.PositiveSmallIntegerField()
    user_lesson_complete = models.ManyToManyField(get_user_model(), related_name='user_lesson_complete')

    class Meta:
        models.UniqueConstraint(fields=['course', 'position'], name='unique_lesson_position')

    def __str__(self):
        return self.title
