from django.shortcuts import get_object_or_404

from accounts.models import Account
from courses.models import Enrollment


def get_user_profile(user_id):
    return get_object_or_404(
        Account.objects.select_related('profile'),
        id=user_id
    )


def get_user_courses(user_id):
    return Enrollment.objects.select_related(
        'course'
    ).only(
        'course__title',
        'course__slug',
        'course__total_points',
        'course__cover'
    ).filter(user_id=user_id)
