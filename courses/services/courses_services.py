from courses.models import Course, Enrollment


def get_completed_lessons(user, course):
    completed_lessons = set()
    if user.is_authenticated:
        completed_lessons = set(
            user.user_lesson_complete.filter(
                course=course
            ).values_list('position', flat=True))
    return completed_lessons


def get_courses():
    return Course.objects.all()


def get_courses_with_tag(tag):
    return Course.objects.filter(tags__tag__iexact=tag).order_by('created_at')


def get_course_with_lessons_and_reviews(course_slug):
    return Course.objects.prefetch_related(
        'lessons',
        'reviews'
    ).get(slug=course_slug)


def get_course_lessons(course):
    return course.lessons.all().order_by('position')


def get_course_reviews(course):
    return course.reviews.all().order_by('created_at')


def is_user_enrolled(user_id, course_id):
    return Enrollment.objects.filter(
            user_id=user_id,
            course_id=course_id
        ).exists()
