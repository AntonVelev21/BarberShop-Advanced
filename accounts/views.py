from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, UserModel
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView
from rest_framework.reverse import reverse_lazy


class RegisterView(CreateView):
    model = UserModel
    form_class = UserCreationForm
    template_name = 'accounts/register.html'

    def get_success_url(self):
        return reverse_lazy('home-page')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)



class LogInView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('home-page')



class LogOutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('home-page')
