from django.urls import path
from . import views

urlpatterns = [
    path("", views.users_root, name="users_root"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("verify/<str:token>/", views.verify_email, name="verify_email"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
]
