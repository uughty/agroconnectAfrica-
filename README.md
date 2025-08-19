# AgroConnect Africa  Development Progress Log

This file documents the step-by-step progress made in setting up and configuring the AgroConnect Africa Django project.



## 1. Project Initialization
- Installed Python and Django.
- Created a virtual environment and activated it.
- Installed required dependencies.
- Started the Django project named **agroconnectAfrica**.
- Created the initial **users** app to handle authentication.



## 2. Database Setup & Migrations
- Configured SQLite as the default database in `settings.py`.
- Ran `makemigrations` and `migrate` to initialize database schema.



## 3. Custom User Model
- Created a `CustomUser` model inheriting from `AbstractUser`.
- Modified the `USERNAME_FIELD` to use **email** instead of username.
- Updated `settings.py` with:
  ```python
  AUTH_USER_MODEL = 'users.CustomUser'
