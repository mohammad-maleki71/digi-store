from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import (
    CouponViewSet,
    ApplyCouponAPIView
)


app_name = "coupons"


router = DefaultRouter()


router.register(
    "coupons",
    CouponViewSet,
    basename="coupon"
)


urlpatterns = [

    path(
        "apply/",
        ApplyCouponAPIView.as_view(),
        name="apply-coupon"
    ),

]


urlpatterns += router.urls