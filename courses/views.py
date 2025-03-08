from django.shortcuts import render

from courses.models import Course


def courses(request):
    all_courses = Course.objects.all()
    context = {
        'courses': all_courses
    }
    return render(request, 'courses/courses.html', context)
