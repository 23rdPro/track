from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=255, required=True, help_text='unique email address')

    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'username')


class CustomUserChangeForm(UserChangeForm):
    email = forms.EmailField(
        max_length=255, required=True, help_text='unique email address')

    class Meta(UserChangeForm):
        model = User
        fields = ('email', 'username')


class UserUpdateAfterSignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', ]
