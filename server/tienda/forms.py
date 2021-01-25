from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# from .models import Profile


class UserRegisterForm(UserCreationForm):
    nombre = forms.CharField(max_length=100)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['nombre', 'username', 'email', 'password1', 'password2']
