from django.http import JsonResponse
from accounts.models import Account
from courses.models import Course, Enrollment


def enroll_course(request):
    if request.method == "POST":
        user_id = request.POST.get('user')
        course_id = request.POST.get('course')

        try:
            course = Course.objects.get(id=course_id)
            user = Account.objects.get(id=user_id)
        except (Course.DoesNotExist, Account.DoesNotExist):
            return JsonResponse({'error': 'Data is incorrect'}, status=400)

        if Enrollment.objects.filter(user=user, course=course).exists():
            return JsonResponse({'error': 'Enrollment already exists'}, status=400)
        else:
            Enrollment.objects.create(user=user, course=course)
            return JsonResponse({'status': 'ok', 'message': 'Subscribe successful'}, status=200)

    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=405)
