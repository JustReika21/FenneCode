from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from lessons.models import Lesson


class BaseTask(models.Model):
    question = models.TextField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.question


class CodeTask(BaseTask):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='code_tasks')
    correct_code = models.CharField(max_length=1024)
    default_code = models.CharField(max_length=1024, blank=True)
    language = models.CharField(
        max_length=20,
        choices=(('Python', 'Python'), ('JavaScript', 'JavaScript'), ('SQL', 'SQL')),
    )
    correct_answer = models.JSONField()


class ChoiceTask(BaseTask):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='choice_tasks')
    choices = models.JSONField()


class Submission(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='submissions')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='submissions')

    task_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name='submissions')
    task_id = models.PositiveIntegerField()
    task = GenericForeignKey('task_type', 'task_id')

    answer = models.JSONField()

    completed = models.BooleanField(default=False)

    class Meta:
        models.UniqueConstraint(fields=['user', 'task'], name='unique_submission')

    def __str__(self):
        return f"{self.user} {self.task} ({self.completed})"
