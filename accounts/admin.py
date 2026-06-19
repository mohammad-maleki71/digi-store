from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Profile
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
)


class ProfileInline(admin.StackedInline):
    model = Profile

@admin.register(User)
class CustomUserAdmin(UserAdmin):

    model = User


    add_form = CustomUserCreationForm


    form = CustomUserChangeForm


    inlines = [
        ProfileInline,
    ]


    ordering = (
        "phone",
    )


    list_display = (
        "phone",
        "email",
        "first_name",
        "last_name",
        "is_admin",
        "is_active",
    )


    search_fields = (
        "phone",
        "email",
    )


    list_filter = (
        "is_admin",
        "is_superuser",
        "is_active",
    )


    fieldsets = (
        (
            None,
            {
                "fields": (
                    "phone",
                    "email",
                    "password",
                )
            }
        ),

        (
            "Personal Info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            }
        ),

        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_admin",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            }
        ),
    )


    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "phone",
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                )
            }
        ),
    )