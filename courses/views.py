from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from courses.forms import EnrollmentForm
from courses.models import Course, Enrollment


def get_completed_lessnons(user):
    completed_lessons = set()
    if user.is_authenticated:
        completed_lessons = set(user.user_lesson_complete.values_list('id', flat=True))
    return completed_lessons


def courses(request):
    all_courses = Course.objects.all()
    context = {
        'courses': all_courses
    }
    return render(request, 'courses/courses.html', context)


def course_info(request, course_slug):
    course = get_object_or_404(Course, slug=course_slug)
    lessons = course.lessons.all()
    reviews = course.reviews.all()
    user = request.user
    completed_lessons = get_completed_lessnons(user)
    is_user_enrolled = Enrollment.objects.filter(user=user).exists()

    if request.method == "POST":
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            if not is_user_enrolled:
                Enrollment.objects.create(user=user, course=course)
                messages.success(request, 'Вы успешно записались на курс')
            else:
                Enrollment.objects.filter(user=user, course=course).delete()
                messages.success(request, 'Вы успешно отписались')
            return redirect(request.path)
    else:
        form = EnrollmentForm()

    context = {
        'course': course,
        'lessons': lessons,
        'reviews': reviews,
        'completed_lessons': completed_lessons,
        'is_user_enrolled': is_user_enrolled,
        'form': form
    }
    return render(request, 'courses/course_info.html', context)
