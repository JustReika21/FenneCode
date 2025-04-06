from django.http import Http404
from django.shortcuts import render

from courses.models import Course, Enrollment


def get_completed_lessons(user, course):
    completed_lessons = set()
    if user.is_authenticated:
        completed_lessons = set(
            user.user_lesson_complete.filter(
                course=course
            ).values_list('position', flat=True))
    return completed_lessons


def courses(request):
    all_courses = Course.objects.all()
    context = {
        'courses': all_courses
    }
    return render(request, 'courses/courses.html', context)


def course_info(request, course_slug):
    try:
        course = Course.objects.prefetch_related('lessons', 'reviews').get(slug=course_slug)
    except Course.DoesNotExist:
        raise Http404
    lessons = course.lessons.all().order_by('position')
    reviews = course.reviews.all().order_by('-created_at')
    user = request.user
    completed_lessons = get_completed_lessons(user, course)
    is_user_enrolled = False
    if user.is_authenticated:
        is_user_enrolled = Enrollment.objects.filter(user=user, course=course).exists()

    rating_choices = [i for i in range(1, 11)]

    context = {
        'course': course,
        'lessons': lessons,
        'reviews': reviews,
        'completed_lessons': completed_lessons,
        'is_user_enrolled': is_user_enrolled,
        'rating_choices': rating_choices
    }
    return render(request, 'courses/course_info.html', context)
