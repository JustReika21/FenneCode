from django.urls import path

from lessons import views

app_name = 'lessons'

urlpatterns = [
    path('<int:lesson_position>/', views.lesson_details, name='lesson_details'),
]
