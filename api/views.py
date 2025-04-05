from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from accounts.models import Account
from courses.models import Course, Enrollment
from lessons.models import Lesson
from reviews.models import Review
from tasks.models import Answer, ChoiceTask, UserChoiceAnswer


def enroll_course(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)
    user_id = request.POST.get('user')
    course_id = request.POST.get('course')

    try:
        course = Course.objects.get(id=course_id)
        user = Account.objects.get(id=user_id)
    except (Course.DoesNotExist, Account.DoesNotExist):
        return JsonResponse({'error': 'Data is incorrect'}, status=400)

    if Enrollment.objects.filter(user=user, course=course).exists():
        return JsonResponse({'error': 'Enrollment already exists'}, status=400)
    else:
        Enrollment.objects.create(user=user, course=course)
        return JsonResponse({'status': 'ok', 'message': 'Subscribe successful'}, status=200)


def submit_choice_task_answers(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)

    task_id = request.POST.get('choice_task')
    user_id = request.POST.get('user')
    answer_ids = request.POST.getlist('selected_answers')

    try:
        user = Account.objects.get(id=user_id)
        task = ChoiceTask.objects.get(id=task_id)
        answers = Answer.objects.filter(choice_task=task)
        user_answers = answers.filter(id__in=answer_ids)

        if not user_answers.exists():
            return JsonResponse({'error': 'Invalid data'}, status=400)

        correct_answers = set(answers.filter(is_correct=True).values_list('id', flat=True))
        chosen_answers = set(user_answers.values_list('id', flat=True))

        correct_user_answers_chosen = list(correct_answers & chosen_answers)
        incorrect_user_answers = list(chosen_answers - correct_answers)
        correct_not_chosen = list(correct_answers - chosen_answers)
        incorrect_not_chosen = list(set(answers.values_list('id', flat=True)) - correct_answers - chosen_answers)

        is_correct = not correct_not_chosen and not incorrect_user_answers

        user_answer = UserChoiceAnswer.objects.create(user=user, choice_task=task, is_correct=is_correct)
        user_answer.selected_answers.set(user_answers)

        return JsonResponse({
            'success': 'Answers submitted',
            'correct_chosen': correct_user_answers_chosen,
            'incorrect_chosen': incorrect_user_answers,
            'incorrect_not_chosen': incorrect_not_chosen,
            'correct_not_chosen': correct_not_chosen
        }, status=200)

    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Data is incorrect'}, status=400)


def check_lesson_completion(request, lesson_id):
    if request.method != "GET":
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)
    try:
        user_id = request.user.id
        lesson = Lesson.objects.prefetch_related('lessons').get(id=lesson_id)
        count_tasks = lesson.lessons.count()
        count_completed_tasks = UserChoiceAnswer.objects.filter(choice_task__lesson=lesson, user=user_id).count()
        is_all_tasks_completed = count_completed_tasks == count_tasks
        return JsonResponse({
            'is_all_tasks_completed': is_all_tasks_completed,
        })
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Data is incorrect'}, status=400)


def mark_lesson_complete(request, lesson_id):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)
    try:
        user_id = request.user.id
        lesson = Lesson.objects.prefetch_related('lessons').get(id=lesson_id)
        lesson.user_lesson_complete.add(user_id)

        enrollment = Enrollment.objects.get(user_id=user_id, course_id=lesson.course_id)
        course = lesson.course
        count_lessons = course.lessons.count()
        count_completed_lessons = course.lessons.filter(user_lesson_complete__id=user_id).count()
        user_progress = count_completed_lessons / count_lessons * 100
        enrollment.progress = round(user_progress, 2)
        enrollment.save(update_fields=["progress"])

        return JsonResponse({'status': 'success'})
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Data is incorrect'}, status=400)


def submit_course_review(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)
    try:
        user = request.user
        course_id = request.POST.get('course')
        text = request.POST.get('text')
        rating = request.POST.get('rating')

        course = Course.objects.get(id=course_id)

        is_user_enrolled = Enrollment.objects.filter(user=user, course=course).exists()
        if not is_user_enrolled:
            return JsonResponse({'error': 'User has not enrolled'}, status=400)

        Review.objects.create(
            user=user,
            course=course,
            text=text,
            rating=rating
        )
        return JsonResponse({
            'success': 'Review left successfully',
            'text': text,
            'rating': rating,
            'username': user.username
        }, status=200)
    except ObjectDoesNotExist:
        return JsonResponse({'error': 'Data is incorrect'}, status=400)
