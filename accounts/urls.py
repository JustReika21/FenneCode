from django.urls import path

from accounts import views

app_name = 'accounts'

urlpatterns = [
    path(
        'signin/',
        views.RegisterView.as_view(),
        name='signin'),
    path(
        'login/',
        views.LoginView.as_view(),
        name='login'
    ),
    path(
        'logout/',
        views.CustomLogoutView.as_view(),
        name='logout'
    ),
]
