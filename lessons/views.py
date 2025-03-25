from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404

from courses.models import Course
from lessons.models import Lesson


@login_required
def lesson_details(request, course_slug, lesson_position):
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, course=course, position=lesson_position)
    user = request.user

    if lesson_position == 1:
        pass
    else:
        prev_lesson = get_object_or_404(Lesson, course=course, position=lesson_position-1)
        user_completed_prev_lesson = prev_lesson.user_lesson_complete.filter(id=user.id).exists()
        if not user_completed_prev_lesson:
            raise PermissionDenied

    # TODO: N+1 для тасков
    code_tasks = lesson.code_tasks.all()
    choice_tasks = lesson.choice_tasks.all()

    context = {
        'lesson': lesson,
        'code_tasks': code_tasks,
        'choice_tasks': choice_tasks,
    }
    return render(request, 'lessons/lesson_details.html', context)
