from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from lessons.models import Lesson


def calculate_course_total_points(instance):
    course = instance.course
    lessons = course.lessons.all()
    course.total_points = sum(lesson.total_points for lesson in lessons)
    course.save()


@receiver(post_save, sender=Lesson)
def update_course_lesson_count_on_save(sender, instance, created, **kwargs):
    if instance.course:
        calculate_course_total_points(instance)


@receiver(post_delete, sender=Lesson)
def update_course_lesson_count_on_delete(sender, instance, created, **kwargs):
    if instance.course:
        calculate_course_total_points(instance)