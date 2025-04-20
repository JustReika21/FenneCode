from collections import defaultdict

from django.shortcuts import get_object_or_404

from courses.models import Course
from lessons.models import Lesson
from tasks.models import ChoiceTask, UserChoiceAnswer


def get_course_by_slug(slug):
    return get_object_or_404(Course, slug=slug)


def get_lesson(course, lesson_position):
    return get_object_or_404(Lesson, course=course, position=lesson_position)


def get_lesson_with_content(course, lesson_position):
    return get_object_or_404(
        Lesson.objects.prefetch_related('content').order_by('position'),
        course=course,
        position=lesson_position
    )


def lesson_exists(course, lesson_position):
    return Lesson.objects.filter(course=course, position=lesson_position).exists()


def is_user_lesson_complete(lesson, user_id):
    return lesson.user_lesson_complete.filter(id=user_id).exists()


def get_all_lesson_tasks(lesson):
    return ChoiceTask.objects.prefetch_related('answers').filter(lesson=lesson).only('id')


def get_choices_for_tasks(tasks):
    return {task.id: list(task.answers.only('id', 'is_correct', 'answer')) for task in tasks}


def get_user_answers_for_tasks(tasks, user_id):
    user_answers = UserChoiceAnswer.objects.filter(
        choice_task__in=tasks, user=user_id
    ).values_list('choice_task_id', 'selected_answers__id')

    answers_dict = defaultdict(set)
    for task_id, selected_answers_id in user_answers:
        answers_dict[task_id].add(selected_answers_id)

    return answers_dict
