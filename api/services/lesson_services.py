from lessons.models import Lesson
from django.shortcuts import get_object_or_404


def get_lesson_with_tasks(lesson_id):
    return get_object_or_404(
        Lesson.objects.prefetch_related('choice_tasks'),
        id=lesson_id
    )


def get_lesson_with_course(lesson_id):
    return get_object_or_404(
        Lesson.objects.select_related('course'),
        id=lesson_id
    )


def get_count_completed_lessons(user_id, course):
    return course.lessons.filter(user_lesson_complete=user_id).count()
