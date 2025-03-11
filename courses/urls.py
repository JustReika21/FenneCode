from django.urls import path
from django.urls.conf import include

from courses import views

app_name = 'courses'

urlpatterns = [
    path('', views.courses, name='courses'),
    path('<slug:course_slug>/', views.course_info, name='course_info'),
    path('<slug:course_slug>/lesson/', include('lessons.urls')),
]
