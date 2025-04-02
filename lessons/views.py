from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404

from courses.models import Course
from lessons.models import Lesson
from tasks.models import ChoiceTask, UserChoiceAnswer
from api.views import check_lesson_completion


@login_required
def lesson_details(request, course_slug, lesson_position):
    # TODO: REFACTOR VIEW, API, TEMPLATE, JS
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, course=course, position=lesson_position)
    user = request.user

    if lesson_position == 1:
        prev_lesson = None
    else:
        prev_lesson = lesson_position - 1
        prev_lesson_object = get_object_or_404(Lesson, course=course, position=prev_lesson)
        user_completed_prev_lesson = prev_lesson_object.user_lesson_complete.filter(id=user.id).exists()
        if not user_completed_prev_lesson:
            raise PermissionDenied

    if Lesson.objects.filter(course=course, position=lesson_position+1).exists():
        next_lesson = lesson_position + 1
    else:
        next_lesson = None

    tasks = ChoiceTask.objects.prefetch_related('answers').filter(lesson=lesson).only('id')

    choices = {task.id: list(task.answers.only('id', 'is_correct', 'answer')) for task in tasks}

    user_answers_dict = {task.id: set(
            UserChoiceAnswer.objects.filter(choice_task=task)
            .values_list('selected_answers__id', flat=True)
        )
        for task in tasks
    }

    count_tasks = len(tasks)
    count_completed_tasks = sum(1 for task in tasks if user_answers_dict.get(task.id))
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
