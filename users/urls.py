#users/urls.py

from django.urls import path
from .views import UserRegistrationView, UserLoginView, CustomLogoutView

app_name = 'users'


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),  # Vista de registro
    path('login/', UserLoginView.as_view(), name='login'),  # Vista de login
    path('logout/', CustomLogoutView.as_view(), name='logout'),
]




