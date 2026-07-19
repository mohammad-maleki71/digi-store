from django.urls import path
from .views import (
    CartAPIView,
    AddToCartAPIView,
    UpdateCartItemAPIView,
    RemoveCartItemAPIView,
)

app_name = "cart"
urlpatterns = [

    path(
        "",
        CartAPIView.as_view(),
        name="cart"
    ),


    path(
        "add/",
        AddToCartAPIView.as_view(),
        name="add-cart"
    ),


    path(
        "items/<int:pk>/",
        UpdateCartItemAPIView.as_view(),
        name="update-item"
    ),

    path(
        "items/<int:pk>/remove/",
        RemoveCartItemAPIView.as_view(),
        name="remove-item"
    ),

]
