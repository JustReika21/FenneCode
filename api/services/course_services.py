from lessons.models import Lesson
from courses.models import Course, Enrollment


def get_course(course_id):
    return Course.objects.get(id=course_id)


def get_course_related_lessons(course_id):
    return Course.objects.prefetch_related('lessons').get(id=course_id)


def get_enrollment(user_id, course_id):
    return Enrollment.objects.get(user_id=user_id, course_id=course_id)


def is_user_enrolled(user_id, course_id):
    return Enrollment.objects.filter(
        user_id=user_id,
        course_id=course_id
    ).exists()


def user_has_access_to_task(user, task):
    cur_lesson = task.lesson
    course = cur_lesson.course

    if cur_lesson.position != 1:
        prev_lesson = Lesson.objects.get(
            position=cur_lesson.position - 1,
            course=course
        )
        if not prev_lesson.user_lesson_complete.filter(id=user.id).exists():
            return False
    else:
        if not is_user_enrolled(user.id, course.id):
            return False

    return True
