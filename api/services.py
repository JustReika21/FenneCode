from courses.models import Enrollment
from lessons.models import Lesson


def is_user_enrolled(user, course):
    return Enrollment.objects.filter(user=user, course=course).exists()


def user_has_access_to_task(user, task):
    cur_lesson = task.lesson
    course = cur_lesson.course

    if cur_lesson.position != 1:
        prev_lesson = Lesson.objects.get(position=cur_lesson.position - 1, course=course)
        if not prev_lesson.user_lesson_complete.filter(id=user).exists():
            return False
    else:
        if not is_user_enrolled(user, course):
            return False

    return True


def evaluate_answers(answers, user_answers):
    correct_answers = set(answers.filter(is_correct=True).values_list('id', flat=True))
    chosen_answers = set(user_answers.values_list('id', flat=True))

    correct_user_answers_chosen = list(correct_answers & chosen_answers)
    incorrect_user_answers = list(chosen_answers - correct_answers)
    correct_not_chosen = list(correct_answers - chosen_answers)
    incorrect_not_chosen = list(set(answers.values_list('id', flat=True)) - correct_answers - chosen_answers)
    is_correct = not correct_not_chosen and not incorrect_user_answers

    return {
        'correct_chosen': correct_user_answers_chosen,
        'incorrect_chosen': incorrect_user_answers,
        'correct_not_chosen': correct_not_chosen,
        'incorrect_not_chosen': incorrect_not_chosen,
        'is_correct': is_correct
    }
