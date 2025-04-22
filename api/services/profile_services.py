from user_profile.models import Profile
from django.shortcuts import get_object_or_404


def get_user_profile(user_id):
    return get_object_or_404(Profile, user_id=user_id)
