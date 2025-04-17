from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render

from lessons.services import LessonService


@login_required
def lesson_details(request, course_slug, lesson_position):
    service = LessonService()
    course = service.get_course_by_slug(course_slug)
    lesson = service.get_lesson(course, lesson_position)
    user = request.user

    prev_lesson = lesson_position - 1 if lesson_position > 1 else None

    if prev_lesson:
        prev_lesson_object = service.get_lesson(course, prev_lesson)
        user_completed_prev_lesson = service.is_user_lesson_complete(
            prev_lesson_object,
            user.id
        )
        if not user_completed_prev_lesson:
            raise PermissionDenied

    next_lesson = lesson_position + 1 if service.lesson_exists(course, lesson_position + 1) else None

    tasks = service.get_all_lesson_tasks(lesson)

    choices = service.get_choices_for_tasks(tasks)

    user_answers_dict = service.get_user_answers_for_tasks(tasks, user.id)

    count_tasks = len(tasks)
    count_completed_tasks = sum(
        1 for task in tasks if user_answers_dict.get(task.id)
    )
    is_all_tasks_completed = count_tasks == count_completed_tasks

    context = {
        'course_slug': course.slug,
        'lesson': lesson,
        'tasks': tasks,
        'choices': choices,
        'user_answers_dict': user_answers_dict,
        'is_all_tasks_completed': is_all_tasks_completed,
        'next_lesson': next_lesson,
        'prev_lesson': prev_lesson,
    }
    return render(request, 'lessons/lesson_details.html', context)
