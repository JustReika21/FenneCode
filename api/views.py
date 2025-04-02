from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from accounts.models import Account
from courses.models import Course, Enrollment
from lessons.models import Lesson
from tasks.models import Answer, ChoiceTask, UserChoiceAnswer


def enroll_course(request):
    if request.method == "POST":
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

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)


def submit_choice_task_answers(request):
    if request.method == "POST":
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

            correct_user_answers_chosen = []
            incorrect_user_answers = []
            incorrect_not_chosen = []
            correct_not_chosen = []

            for answer in user_answers.all():
                if answer.is_correct:
                    correct_user_answers_chosen.append(answer.id)
                else:
                    incorrect_user_answers.append(answer.id)

            for answer in answers.all():
                if answer.is_correct and answer.id not in correct_user_answers_chosen:
                    correct_not_chosen.append(answer.id)
                elif not answer.is_correct and answer.id not in incorrect_user_answers:
                    incorrect_not_chosen.append(answer.id)

            is_correct = not correct_not_chosen and not incorrect_user_answers

            user_answer = UserChoiceAnswer.objects.create(user=user, choice_task=task, is_correct=is_correct)
            user_answer.selected_answers.set(user_answers)

            return JsonResponse({
                'success': 'Answers submitted',
                'correct_chosen': correct_user_answers_chosen,
                'incorrect_chosen': incorrect_user_answers,
                'incorrect_not_chosen': incorrect_not_chosen,
                'correct_not_chosen': correct_not_chosen
            },
                status=200)

        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Data is incorrect'}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)


def check_lesson_completion(request, lesson_id):
    if request.method == "GET":
        try:
            user_id = request.user.id
            lesson = Lesson.objects.get(id=lesson_id)
            count_tasks = lesson.lessons.count()
            count_completed_tasks = UserChoiceAnswer.objects.filter(choice_task__lesson=lesson, user=user_id).count()
            return JsonResponse({
                'is_all_tasks_completed': count_completed_tasks == count_tasks
            })
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Data is incorrect'}, status=400)
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)

