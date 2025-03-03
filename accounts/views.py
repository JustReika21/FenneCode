from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.views.generic import FormView
from accounts.forms import RegistrationForm


class RegisterView(FormView):
    form_class = RegistrationForm
    template_name = 'registration/signup.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'


class CustomLogoutView(LogoutView):
    pass
