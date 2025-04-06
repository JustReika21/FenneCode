from django.urls import path

from user_profile import views

app_name = 'user_profile'

urlpatterns = [
    path('<int:user_id>', views.profile, name='profile'),
    path('<int:user_id>/edit', views.edit_profile, name='edit_profile'),
]
