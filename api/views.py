from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST
import subprocess


from accounts.models import Account
from api.services.code_runner_services import (
    validate_ast,
    limit_resources, UnsafeCodeError
)
from api.services.course_services import (
    get_course,
    get_course_related_lessons,
    get_enrollment,
    is_user_enrolled,
    user_has_access_to_task
)
from api.services.lesson_services import (
    get_lesson_with_tasks,
    get_lesson_with_course,
    get_count_completed_lessons,
)
from api.services.profile_services import get_user_profile
from api.services.task_services import (
    get_task_with_course,
    get_task_answers,
    get_filtered_user_answers,
    get_count_tasks_in_lesson,
    evaluate_answers
)

from courses.models import Course, Enrollment
from reviews.models import Review
from tasks.models import UserChoiceAnswer

from user_profile.forms import ProfileEditForm
from reviews.forms import ReviewForm


@require_POST
@login_required
def enroll_course(request):
    course_id = request.POST.get('course')
    user = request.user

    try:
        course = get_course(course_id)
    except (Course.DoesNotExist, Account.DoesNotExist):
        return JsonResponse({
            'status': 'error',
            'message': 'Неверные данные'
        }, status=400)

    if is_user_enrolled(user.id, course.id):
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
    try:
        answer_ids = tuple(map(int, request.POST.getlist('selected_answers')))
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
    task = get_task_with_course(task_id)

    if not user_has_access_to_task(user, task):
        return JsonResponse({
            'status': 'error',
            'message': 'У вас нет доступа к этому заданию'
        }, status=403)

    answers = get_task_answers(task_id)
    user_answers = get_filtered_user_answers(answers, answer_ids)

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
        try:
            enrollment = get_enrollment(user.id, task.lesson.course.id)
            enrollment.points += points
            enrollment.save()
        except Enrollment.DoesNotExist:
            return JsonResponse({
                'status': 'error',
                'message': 'Вы должны быть записаны на курс'
            }, status=403)

    user_answer = UserChoiceAnswer.objects.create(
        user=user, choice_task=task, points=points
    )
    user_answer.selected_answers.set(user_answers)

    return JsonResponse({
        'status': 'success',
        'message': 'Ответы сохранены',
        **result_answers
    }, status=200)


@require_POST
@login_required
def run_code(request):
    try:
        code = request.POST.get('code')
        validate_ast(code)

        result = subprocess.run(
            ['python3', '-c', code],
            capture_output=True,
            text=True,
            timeout=5,
            preexec_fn=limit_resources,
            env={'PYTHONSAFEPATH': '/tmp'},
            cwd='/tmp',
        )
        if result.returncode != 0:
            return JsonResponse({
                "status": "error",
                "console_output": result.stderr or 'Execution aborted'
            }, status=400)

        return JsonResponse({
            "status": "success",
            "console_output": result.stderr or result.stdout or 'Execution failed'
        }, status=200)

    except UnsafeCodeError as e:
        return JsonResponse({
            "status": "error",
            "console_output": str(e)
        }, status=403)
    except subprocess.TimeoutExpired:
        return JsonResponse({
            "status": "error",
            "console_output": "Execution timed out"
        }, status=408)
    except Exception as e:
        return JsonResponse({
            "status": "error",
            "console_output": str(e)
        }, status=400)


@require_GET
@login_required
def check_lesson_completion(request, lesson_id):

    user = request.user
    lesson = get_lesson_with_tasks(lesson_id)

    count_tasks = lesson.choice_tasks.count()
    count_completed_tasks = get_count_tasks_in_lesson(user.id, lesson_id)
    is_all_tasks_completed = count_completed_tasks == count_tasks

    return JsonResponse({
        'status': 'success',
        'is_all_tasks_completed': is_all_tasks_completed,
    })


@require_POST
@login_required
def mark_lesson_complete(request, lesson_id):
    lesson = get_lesson_with_course(lesson_id)
    user = request.user

    try:
        enrollment = get_enrollment(user.id, lesson.course.id)
    except Enrollment.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Вы должны быть записаны на курс'
        }, status=403)

    lesson.user_lesson_complete.add(user)

    course_with_lessons = get_course_related_lessons(lesson.course.id)

    total_lessons = course_with_lessons.lessons.count()
    total_completed_lessons = get_count_completed_lessons(
        user.id,
        course_with_lessons
    )
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
    course_id = request.POST.get('course')

    form = ReviewForm(request.POST)
    user = request.user
    if not form.is_valid():
        return JsonResponse({
            'status': 'error',
            'errors': form.errors.get_json_data()
        }, status=400)

    try:
        course = get_course(course_id)
    except Course.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'errors': 'Курс не существует'
        }, status=404)

    if not is_user_enrolled(user.id, course.id):
        return JsonResponse({
            'status': 'error',
            'errors': 'Вы не записаны на курс'
        }, status=403)

    review = form.save()
    return JsonResponse({
        'status': 'success',
        'message': 'Вы успешно оставили отзыв',
        'review': {
            'text': review.text,
            'rating': review.rating,
            'username': user.username,
            'review_id': review.id,
        },
    }, status=200)


@require_POST
@login_required
def delete_course_review(request, review_id):
    user = request.user
    review = Review.objects.filter(
        user_id=user.id,
        id=review_id
    ).first()
    if review:
        review.delete()
        return JsonResponse({
            'status': 'success',
            'message': 'Вы удалили отзыв'
        }, status=200)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Отзыва не существует'
        }, status=404)


@require_POST
@login_required
def edit_profile(request):

    user = request.user
    user_profile = get_user_profile(user.id)

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
