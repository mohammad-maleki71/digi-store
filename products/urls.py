from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet,
    BrandViewSet,
    ProductViewSet,
    ProductImageViewSet,
)


app_name = "products"

router = DefaultRouter()

router.register(
    "categories",
    CategoryViewSet,
    basename="category",
)

router.register(
    "brands",
    BrandViewSet,
    basename="brand",
)

router.register(
    "products",
    ProductViewSet,
    basename="product",
)

router.register(
    "images",
    ProductImageViewSet,
    basename="product-image",
)

urlpatterns = router.urls


