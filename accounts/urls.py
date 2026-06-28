from django.urls import path

from .views import (
    UserRegisterAPIView,
    PhoneVerificationAPIView,
    EmailVerificationAPIView,
)


app_name = "accounts"
urlpatterns = [

    path(
        "register/",
        UserRegisterAPIView.as_view(),
        name="register"
    ),

    path(
        "verify-phone/",
        PhoneVerificationAPIView.as_view(),
        name="verify-phone"
    ),

    path(
        "verify-email/",
        EmailVerificationAPIView.as_view(),
        name="verify-email"
    ),

]

