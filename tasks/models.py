from django.db import models

from fennecode import settings
from lessons.models import Lesson


class ChoiceTask(models.Model):
    lesson = models.ForeignKey(
        Lesson,
        related_name='choice_tasks',
        on_delete=models.CASCADE
    )
    points = models.SmallIntegerField(default=10)
    question = models.TextField()

    def __str__(self):
        return f'Урок:{self.lesson} Вопрос: {self.question}'


class Answer(models.Model):
    choice_task = models.ForeignKey(
        ChoiceTask,
        related_name='answers',
        on_delete=models.CASCADE
    )
    answer = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.answer} ({'Верно' if self.is_correct else 'Неверно'})"


class UserChoiceAnswer(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='user_choice_answers',
        on_delete=models.CASCADE
    )
    choice_task = models.ForeignKey(
        ChoiceTask,
        related_name='user_choice_answers',
        on_delete=models.CASCADE
    )
    selected_answers = models.ManyToManyField(
        Answer,
        related_name='user_choice_answers'
    )
    points = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'Пользователь: {self.choice_task}, Задание: {self.choice_task}'

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'choice_task'],
                name='unique_user_choice_answer'
            ),
        ]
