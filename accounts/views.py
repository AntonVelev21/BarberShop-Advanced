from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, UserModel
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.views.generic import CreateView
from rest_framework.reverse import reverse_lazy
from accounts.forms import UserProfileCreationForm

#TO DO
#Implement logic to add phone number field when creating user
class RegisterView(CreateView):
    model = UserModel
    template_name = 'accounts/register.html'
    form_class = UserCreationForm

    def get_success_url(self):
        return reverse_lazy('home-page')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())



class LogInView(LoginView):
    template_name = 'accounts/login.html'

    def get_success_url(self):
        return reverse_lazy('home-page')



class LogOutView(LogoutView):
    def get_success_url(self):
        return reverse_lazy('home-page')
