from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser


# Registration form
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser   # 🔥 use the correct model
        fields = ("email", "password1", "password2")  # no username


# Login form
class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email")  # Treat email as username
