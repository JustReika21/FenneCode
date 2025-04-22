from tasks.models import ChoiceTask, Answer, UserChoiceAnswer
from lessons.models import Lesson
from django.shortcuts import get_object_or_404


def get_task_with_course(task_id):
    return get_object_or_404(
        ChoiceTask.objects.select_related("lesson__course"),
        id=task_id
    )


def get_task_answers(task_id):
    return Answer.objects.filter(choice_task_id=task_id)


def get_filtered_user_answers(answers, answer_ids):
    return answers.filter(id__in=answer_ids)


def get_count_tasks_in_lesson(user_id, lesson_id):
    return UserChoiceAnswer.objects.filter(
        choice_task__lesson_id=lesson_id,
        user_id=user_id
    ).count()


def evaluate_answers(answers, user_answers):
    correct_answers = set(
        answers.filter(is_correct=True).values_list('id', flat=True)
    )
    chosen_answers = set(user_answers.values_list('id', flat=True))

    correct_user_answers_chosen = list(correct_answers & chosen_answers)
    incorrect_user_answers = list(chosen_answers - correct_answers)
    correct_not_chosen = list(correct_answers - chosen_answers)
    incorrect_not_chosen = list(
        set(answers.values_list('id', flat=True)) - correct_answers - chosen_answers
    )
    is_correct = not correct_not_chosen and not incorrect_user_answers

    return {
        'correct_chosen': correct_user_answers_chosen,
        'incorrect_chosen': incorrect_user_answers,
        'correct_not_chosen': correct_not_chosen,
        'incorrect_not_chosen': incorrect_not_chosen,
        'is_correct': is_correct
    }
