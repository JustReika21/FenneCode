from django.shortcuts import render

from accounts.models import Account
from courses.models import Enrollment


def profile(request, user_id):
    user_profile = Account.objects.get(id=user_id)
    user_courses = Enrollment.objects.select_related(
        'course'
    ).only(
        'course__title',
        'course__slug',
        'course__cover'
    ).filter(user_id=user_id)

    context = {
        'user_profile': user_profile,
        'user_courses': user_courses,
    }
    return render(request, 'user_profile/profile.html', context)
