# users/views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db import transaction
from .tokens import make_email_token, read_email_token
from django.shortcuts import render
from django.db import IntegrityError



def users_root(request):
    # If logged in, go to dashboard. Else, open the combined login/register page.
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "users/login.html")

def _get_username_from_email(email: str) -> str:
    # A simple helper in case you want to autogenerate usernames (not used now).
    return email.split("@")[0]

@transaction.atomic
def register_view(request):
    if request.method != "POST":
        return redirect("users_root")

    email = (request.POST.get("email") or "").strip().lower()
    username = (request.POST.get("username") or "").strip()
    password = (request.POST.get("password") or "").strip()
    confirm  = (request.POST.get("confirm_password") or "").strip()

    if not all([email, username, password, confirm]):
        messages.error(request, "Please fill in all registration fields.")
        return redirect("users_root")

    if password != confirm:
        messages.error(request, "Passwords do not match.")
        return redirect("users_root")

    if User.objects.filter(email__iexact=email).exists():
        messages.error(request, "An account with that email already exists.")
        return redirect("users_root")

    if User.objects.filter(username__iexact=username).exists():
        messages.error(request, "That username is already taken.")
        return redirect("users_root")

    # Create user as inactive until email is verified
    user = User.objects.create_user(username=username, email=email, password=password, is_active=False)

    # Build verification link
    token = make_email_token(user.id)
    verify_url = request.build_absolute_uri(reverse("verify_email", args=[token]))

    # Send email (console backend prints to terminal)
    subject = "Verify your GreenChain account"
    body = f"Hi {username},\n\nPlease verify your account by clicking this link:\n{verify_url}\n\nIf you didn’t request this, ignore this email."
    send_mail(subject, body, None, [email], fail_silently=False)

    messages.success(request, f"Registration successful! Check {email} for a verification link.")
    return redirect("users_root")

def login_view(request):
    if request.method != "POST":
        return redirect("users_root")

    email = (request.POST.get("email") or "").strip().lower()
    password = (request.POST.get("password") or "").strip()

    if not email or not password:
        messages.error(request, "Please enter both email and password.")
        return redirect("users_root")

    # Authenticate by email: find username then authenticate
    try:
        user = User.objects.get(email__iexact=email)
    except User.DoesNotExist:
        messages.error(request, "Invalid credentials.")
        return redirect("users_root")

    user_auth = authenticate(request, username=user.username, password=password)
    if user_auth is None:
        messages.error(request, "Invalid credentials.")
        return redirect("users_root")

    if not user_auth.is_active:
        messages.error(request, "Your account is not verified yet. Check your email.")
        return redirect("users_root")

    login(request, user_auth)
    return redirect("dashboard")

def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("users_root")

def verify_email(request, token: str):
    uid = read_email_token(token)
    if not uid:
        messages.error(request, "Invalid or expired verification link.")
        return redirect("users_root")

    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        messages.error(request, "Invalid verification link.")
        return redirect("users_root")

    if user.is_active:
        messages.info(request, "Your account is already verified. You can log in.")
        return redirect("users_root")

    user.is_active = True
    user.save(update_fields=["is_active"])
    messages.success(request, "Email verified! You can now log in.")
    return redirect("users_root")

@login_required
def dashboard_view(request):
    return render(request, "users/dashboard.html")

from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

def register_view(request):
    User = get_user_model()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  
    else:
        form = UserCreationForm()

    context = {'form': form}  # ✅ define context here

def register_view(request):
    
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "").strip()
        username = request.POST.get("username", "").strip()

        # Fallback: if username is empty, use email before the @
        if not username:
            username = email.split("@")[0]

        # Make sure username is unique
        original_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{original_username}_{counter}"
            counter += 1

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, "Account created successfully! Please log in.")
            return redirect("login")  # change 'login' to your login URL name
        except IntegrityError:
            messages.error(request, "This email is already registered.")
        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")

    return render(request, "register.html")


# users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django import forms

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'email']

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password1")
        p2 = cleaned_data.get("password2")
        if p1 != p2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['email'],  # use email as username
                email=form.cleaned_data['email'],
                first_name=form.cleaned_data['first_name'],
                password=form.cleaned_data['password1']
            )
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('home')  # redirect to home page after register
    else:
        form = RegisterForm()
    return render(request, "users/register.html", {"form": form})

from .forms import CustomUserCreationForm

def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Require verification before login
            user.save()
            # send email verification here
            return redirect('login')  # Or wherever you want
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('username')  # This is actually the email field in your form
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # 'dashboard' should be the name of your URL pattern
        else:
            messages.error(request, 'Invalid email or password')

    return render(request, 'login.html')

@login_required
def dashboard_view(request):
    return render(request, "dashboard.html")