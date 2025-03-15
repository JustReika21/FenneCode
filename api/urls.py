from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api import views

app_name = 'api'

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),
    path('enroll/', views.enroll_course, name='enroll_course'),
]
