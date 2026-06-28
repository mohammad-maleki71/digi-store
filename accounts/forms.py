from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.html import format_html

from .models import User


class CustomUserCreationForm(forms.ModelForm):

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput
    )


    class Meta:
        model = User

        fields = (
            "phone",
            "email",
            "first_name",
            "last_name",
        )


    def clean(self):

        cleaned_data = super().clean()

        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                "Passwords do not match"
            )

        return cleaned_data


    def save(self, commit=True):

        user = super().save(commit=False)

        user.set_password(
            self.cleaned_data["password1"]
        )

        if commit:
            user.save()

        return user



class CustomUserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField(
        help_text=format_html(
            ' please change  your password by this link: ',
            '<a href="../password/">Change password</a>'
        )
    )


    class Meta:
        model = User

        fields = (
            "phone",
            "email",
            "first_name",
            "last_name",
            "password",
            "is_active",
            "is_staff",
            "is_admin",
            "is_superuser",
            "groups",
            "user_permissions",
            "phone_verified",
            "email_verified",
        )