from django.urls import path

from accounts.views import RegisterView, LogInView, LogOutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout')
]