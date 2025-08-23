# agroconnect/users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

# Registration form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "password1", "password2")  # ✅ remove 'username'

# Login form
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")  # Treat email as username
