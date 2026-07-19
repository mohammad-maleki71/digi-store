from django.urls import path
from .views import (
    CreateShippingAddressAPIView,
    ShipmentDetailAPIView,
)

app_name = "shipping"
urlpatterns = [

    path(
        "address/",
        CreateShippingAddressAPIView.as_view(),
        name="create-address"
    ),


    path(
        "orders/<int:order_id>/shipment/",
        ShipmentDetailAPIView.as_view(),
        name="shipment-detail"
    ),

]