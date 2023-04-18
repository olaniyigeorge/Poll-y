from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    #email = forms.EmailField(max_length=120, help_text="Required. Type in your email")
    #Add additional fields to request for on sign up

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')