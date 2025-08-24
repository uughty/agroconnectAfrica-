from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.users_root, name="users_root"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),  # redirect after logout
    path("verify/<str:token>/", views.verify_email, name="verify_email"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
]
