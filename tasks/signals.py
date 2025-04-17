from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ChoiceTask


def calculate_lesson_total_points(lesson):
    tasks = lesson.choice_tasks.all()
    lesson.total_points = sum(task.points for task in tasks)
    lesson.save()


@receiver(post_save, sender=ChoiceTask)
def update_lesson_total_points_on_save(sender, instance, **kwargs):
    if instance.lesson:
        calculate_lesson_total_points(instance.lesson)


@receiver(post_delete, sender=ChoiceTask)
def update_lesson_total_points_on_delete(sender, instance, **kwargs):
    if instance.lesson:
        calculate_lesson_total_points(instance.lesson)
