from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    UserRegisterAPIView,
    PhoneVerificationAPIView,
    EmailVerificationAPIView,
    LoginAPIView,
    LogoutAPIView,
    ProfileAPIView,

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

    path("login/", LoginAPIView.as_view(), name="login"),

    path("logout/", LogoutAPIView.as_view(), name="logout"),

    path("refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("profile/", ProfileAPIView.as_view(), name="profile"),

]

