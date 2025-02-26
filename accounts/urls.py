from django.urls import path

from accounts import views

urlpatterns = [
    path('signin/', views.RegisterView.as_view(), name='signin'),
]