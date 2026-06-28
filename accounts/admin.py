from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Profile
from .forms import (
    CustomUserCreationForm,
    CustomUserChangeForm,
)


class ProfileInline(admin.StackedInline):
    model = Profile
    extra = 0
    max_num = 1

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
        "is_active",
        "is_staff",
        "phone_verified",
        "email_verified",
        "is_admin",
    )


    search_fields = (
        "phone",
        "email",
    )

    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "is_admin",
        "phone_verified",
        "email_verified",
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
                    "is_staff",
                    "is_admin",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                    "phone_verified",
                    "email_verified",
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
                    "is_staff",
                    "is_admin",
                    "is_active",
                )
            }
        ),
    )