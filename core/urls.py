from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('forbidden/', views.custom_handler403, name='handler403'),
]
