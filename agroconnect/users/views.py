# users/views.py
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.db import transaction, IntegrityError
from django.shortcuts import redirect, render
from django.urls import reverse
from django import forms

from .tokens import make_email_token, read_email_token
from .forms import CustomUserCreationForm  # assuming you have this

User = get_user_model()


# ===========================
# HOME + ROOT
# ===========================
def home(request):
    return render(request, "home.html")


def users_root(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    return render(request, "users/login.html")


# ===========================
# REGISTER
# ===========================
@transaction.atomic
def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # require verification
            user.save()

            # Generate email verification link
            token = make_email_token(user.id)
            verify_url = request.build_absolute_uri(reverse("verify_email", args=[token]))

            subject = "Verify your GreenChain account"
            body = f"Hi {user.username},\n\nClick here to verify your account:\n{verify_url}"
            send_mail(subject, body, None, [user.email], fail_silently=False)

            messages.success(request, f"Account created! Check {user.email} for verification link.")
            return redirect("login")
    else:
        form = CustomUserCreationForm()

    return render(request, "register.html", {"form": form})


# ===========================
# LOGIN
# ===========================
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "").strip()

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return redirect("login")

        user_auth = authenticate(request, username=user_obj.username, password=password)
        if user_auth is None:
            messages.error(request, "Invalid email or password")
            return redirect("login")

        if not user_auth.is_active:
            messages.error(request, "Account not verified. Check your email.")
            return redirect("login")

        login(request, user_auth)
        return redirect("dashboard")

    return render(request, "users/login.html")


# ===========================
# LOGOUT
# ===========================
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logged out successfully.")
    return redirect("login")


# ===========================
# VERIFY EMAIL
# ===========================
def verify_email(request, token: str):
    uid = read_email_token(token)
    if not uid:
        messages.error(request, "Invalid or expired verification link.")
        return redirect("login")

    try:
        user = User.objects.get(id=uid)
    except User.DoesNotExist:
        messages.error(request, "Invalid verification link.")
        return redirect("login")

    if user.is_active:
        messages.info(request, "Your account is already verified.")
        return redirect("login")

    user.is_active = True
    user.save(update_fields=["is_active"])
    messages.success(request, "Email verified! You can now log in.")
    return redirect("login")


# ===========================
# DASHBOARD
# ===========================
@login_required(login_url="login")
def dashboard_view(request):
    return render(request, "users/dashboard.html")
