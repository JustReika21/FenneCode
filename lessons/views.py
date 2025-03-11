from django.shortcuts import render, get_object_or_404

from lessons.models import Lesson


def lesson_details(request, course_slug, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)

    # TODO: N+1 для тасков
    code_tasks = lesson.code_tasks.all()
    choice_tasks = lesson.choice_tasks.all()

    context = {
        'lesson': lesson,
        'code_tasks': code_tasks,
        'choice_tasks': choice_tasks,
    }
    return render(request, 'lessons/lesson_details.html', context)
