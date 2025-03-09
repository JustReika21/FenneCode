from django.shortcuts import render, get_object_or_404

from courses.models import Course


def courses(request):
    all_courses = Course.objects.all()
    context = {
        'courses': all_courses
    }
    return render(request, 'courses/courses.html', context)


def course_info(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    lessons = course.lessons.all()
    context = {
        'course': course,
        'lessons': lessons
    }
    return render(request, 'courses/course_info.html', context)
