from accounts.models import Account
from courses.models import Enrollment


def get_user_profile(user_id):
    return Account.objects.select_related('profile').get(id=user_id)


def get_user_courses(user_id):
    return Enrollment.objects.select_related(
        'course'
    ).only(
        'course__title',
        'course__slug',
        'course__total_points',
        'course__cover'
    ).filter(user_id=user_id)
