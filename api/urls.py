from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

app_name = 'api'

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('enroll/', views.enroll_course, name='enroll_course'),
    path(
        'submit_choice_task_answer/',
        views.submit_choice_task_answers,
        name='submit_choice_task_answers'
    ),
    path(
        'check_lesson_completion/<int:lesson_id>',
        views.check_lesson_completion,
        name='check_lesson_completion'
    )
]
