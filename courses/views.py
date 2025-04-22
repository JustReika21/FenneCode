from django.http import Http404
from django.shortcuts import render

from courses.services.courses_services import (
    get_completed_lessons,
    get_courses_with_tag,
    get_courses, get_course_with_lessons_and_reviews, get_course_lessons,
    get_course_reviews, is_user_enrolled
)
from courses.models import Course


def courses(request):
    tag = request.GET.get('tag')
    if tag:
        all_courses = get_courses_with_tag(tag)
    else:
        all_courses = get_courses()
    context = {
        'courses': all_courses
    }
    return render(request, 'courses/courses.html', context)


def course_info(request, course_slug):
    try:
        course = get_course_with_lessons_and_reviews(course_slug)
    except Course.DoesNotExist:
        raise Http404
    lessons = get_course_lessons(course)
    reviews = get_course_reviews(course)
    user = request.user
    completed_lessons = get_completed_lessons(user, course)
    is_enrolled = False
    if user.is_authenticated:
        is_enrolled = is_user_enrolled(user.id, course.id)

    rating_choices = [i for i in range(1, 11)]

    context = {
        'course': course,
        'lessons': lessons,
        'reviews': reviews,
        'completed_lessons': completed_lessons,
        'is_user_enrolled': is_enrolled,
        'rating_choices': rating_choices
    }
    return render(request, 'courses/course_info.html', context)
