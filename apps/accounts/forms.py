from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="CPF ou Email", max_length=254)

class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "cpf", "first_name", "last_name", "role")

