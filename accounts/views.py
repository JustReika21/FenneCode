from django.contrib.auth.views import LoginView
from django.views.generic import FormView
from accounts.forms import RegistrationForm


class RegisterView(FormView):
    form_class = RegistrationForm
    template_name = 'registration/signup.html'
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
