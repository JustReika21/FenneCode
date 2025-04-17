from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST

from accounts.models import Account
from api.services import (
    user_has_access_to_task,
    evaluate_answers,
    is_user_enrolled
)
from courses.models import Course, Enrollment
from lessons.models import Lesson
from tasks.models import Answer, ChoiceTask, UserChoiceAnswer
from user_profile.models import Profile

from user_profile.forms import ProfileEditForm
from reviews.forms import ReviewForm


@require_POST
@login_required
def enroll_course(request):
    course_id = request.POST.get('course')
    user = request.user

    try:
        course = Course.objects.get(id=course_id)
    except (Course.DoesNotExist, Account.DoesNotExist):
        return JsonResponse({
            'status': 'error',
            'message': 'Неверные данные'
        }, status=400)

    if is_user_enrolled(user, course):
        return JsonResponse({
            'status': 'error',
            'message': 'Вы уже записаны на курс'
        }, status=403)
    else:
        Enrollment.objects.create(user=user, course=course)
        return JsonResponse({
            'status': 'success',
            'message': 'Вы успешно записались на курс'
        }, status=200)


@require_POST
@login_required
def submit_choice_task_answers(request):
    if request.method != 'POST':
        return JsonResponse({
            'status': 'error',
            'message': 'Неверный запрос'
        }, status=405)

    try:
        answer_ids = list(map(int, request.POST.getlist('selected_answers')))
        task_id = int(request.POST.get('choice_task'))
    except (TypeError, ValueError):
        return JsonResponse({
            'status': 'error',
            'message': 'Некорректные идентификаторы ответов'
        }, status=400)

    if not task_id or not answer_ids:
        return JsonResponse({
            'status': 'error',
            'message': 'Неверные данные'
        }, status=400)

    user = request.user
    task = get_object_or_404(ChoiceTask.objects.select_related("lesson__course"), id=task_id)

    if not user_has_access_to_task(user, task):
        return JsonResponse({
            'status': 'error',
            'message': 'У вас нет доступа к этому заданию'
        }, status=403)

    answers = Answer.objects.filter(choice_task=task)
    user_answers = answers.filter(id__in=answer_ids)

    if not user_answers.exists():
        return JsonResponse({
            'status': 'error',
            'message': 'Данные об ответах некорректны'
        }, status=400)

    result_answers = evaluate_answers(answers, user_answers)

    is_correct = result_answers['is_correct']
    points = 0
    if is_correct:
        points = task.points
        enrollment = Enrollment.objects.get(
            user=user,
            course=task.lesson.course
        )
        enrollment.points += points
        enrollment.save()

    user_answer = UserChoiceAnswer.objects.create(
        user=user, choice_task=task, points=points
    )
    user_answer.selected_answers.set(user_answers)

    return JsonResponse({
        'status': 'success',
        'message': 'Ответы сохранены',
        **result_answers
    }, status=200)


@require_GET
@login_required
def check_lesson_completion(request, lesson_id):
    try:
        lesson = Lesson.objects.prefetch_related(
            'choice_tasks'
        ).get(id=lesson_id)
    except Lesson.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Такого урока не существует'
        })
    user = request.user

    count_tasks = lesson.choice_tasks.count()
    count_completed_tasks = UserChoiceAnswer.objects.filter(
        choice_task__lesson=lesson,
        user=user
    ).count()
    is_all_tasks_completed = count_completed_tasks == count_tasks
    return JsonResponse({
        'status': 'success',
        'is_all_tasks_completed': is_all_tasks_completed,
    })


@require_POST
@login_required
def mark_lesson_complete(request, lesson_id):
    lesson = get_object_or_404(
        Lesson.objects
        .select_related('course')
        .prefetch_related('course__lessons'),
        id=lesson_id
    )
    user = request.user

    try:
        enrollment = Enrollment.objects.get(user=user, course=lesson.course)
    except Enrollment.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Вы должны быть записаны на курс'
        }, status=403)

    if lesson.user_lesson_complete.filter(id=user.id).exists():
        return JsonResponse({
            'status': 'error',
            'message': 'Вы уже завершили этот урок'
        }, status=403)
    lesson.user_lesson_complete.add(user)

    total_lessons = lesson.course.lessons.count()
    total_completed_lessons = lesson.course.lessons.filter(
        user_lesson_complete=user
    ).count()
    user_progress = total_completed_lessons / total_lessons * 100
    enrollment.progress = round(user_progress, 2)
    enrollment.save(update_fields=["progress"])

    return JsonResponse({
        'status': 'success',
        'message': 'Урок успешно отмечен как пройденный'
    }, status=200)


@require_POST
@login_required
def submit_course_review(request):
    if request.method != "POST":
        return JsonResponse({
            'status': 'error',
            'message': 'Неверный запрос'
        }, status=405)

    form = ReviewForm(request.POST)
    user = request.user
    if not form.is_valid():
        return JsonResponse({
            'status': 'error',
            'errors': form.errors.get_json_data()
        }, status=400)

    try:
        course = Course.objects.get(id=request.POST.get('course'))
    except Course.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'errors': 'Курс не существует'
        }, status=400)

    if not Enrollment.objects.filter(user=user, course=course).exists():
        return JsonResponse({
            'status': 'error',
            'errors': 'Вы не записаны на курс'
        }, status=400)

    review = form.save()
    return JsonResponse({
        'status': 'success',
        'message': 'Вы успешно оставили отзыв',
        'review': {
            'text': review.text,
            'rating': review.rating,
            'username': user.username
        }
    }, status=200)


@require_POST
@login_required
def edit_profile(request):
    if request.method != "POST":
        return JsonResponse({
            'status': 'error',
            'message': 'Неверный запрос'
        }, status=405)

    user = request.user
    user_profile = get_object_or_404(Profile, user=user)

    form = ProfileEditForm(request.POST, request.FILES, instance=user_profile)
    if not form.is_valid():
        return JsonResponse({
            'status': 'error',
            'message': 'Неверные данные',
            'errors': form.errors
        }, status=400)

    form.save()
    return JsonResponse({
        'status': 'success',
        'message': 'Профиль успешно обновлен'
    }, status=200)
