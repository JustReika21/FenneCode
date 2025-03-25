from django.shortcuts import render


def home(request):
    return render(request, 'core/index.html')


def custom_handler403(request, *args, **kwargs):
    return render(request, 'core/403.html', status=403)
