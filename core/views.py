from django.shortcuts import render


def home(request):
    return render(request, 'core/index.html')


def custom_handler403(request, *args, **kwargs):
    return render(request, 'core/403.html', status=403)


def custom_handler404(request, *args, **kwargs):
    return render(request, 'core/404.html', status=404)


def custom_handler500(request, *args, **kwargs):
    return render(request, 'core/500.html', status=500)
