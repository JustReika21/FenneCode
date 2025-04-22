from django.shortcuts import render

from user_profile.services.user_profile_services import (
    get_user_courses,
    get_user_profile
)


def profile(request, user_id):
    user_profile = get_user_profile(user_id)
    user_courses = get_user_courses(user_id)

    context = {
        'user_profile': user_profile,
        'user_courses': user_courses,
    }
    return render(request, 'user_profile/profile.html', context)


def edit_profile(request, user_id):
    return render(request, 'user_profile/edit_profile.html')
