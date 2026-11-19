from django.contrib.auth.forms import (
    AdminUserCreationForm,
    UserChangeForm,
    UserCreationForm,
)

from .models import CustomUser


# Used by the public sign-up page
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "zip",
        )


# Used by the admin "Add user" page (Django 5.1+ needs AdminUserCreationForm)
class CustomAdminUserCreationForm(AdminUserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "zip",
        )


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "email",
            "zip",
        )
