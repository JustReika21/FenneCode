from django.db import models

from courses.models import Course


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='courses')
    title = models.CharField(max_length=100)
    content = models.TextField()
    position = models.PositiveSmallIntegerField()

    class Meta:
        models.UniqueConstraint(fields=['course', 'position'], name='unique_lesson_position')

    def __str__(self):
        return self.title
