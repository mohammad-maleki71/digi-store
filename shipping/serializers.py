from rest_framework import serializers
from .models import Shipment
from .models import ShippingAddress


class ShippingAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShippingAddress

        fields = (
            "id",
            "order",
            "full_name",
            "phone",
            "province",
            "city",
            "address",
            "postal_code",
            "created_at",
        )

        read_only_fields = (
            "id",
            "created_at",
        )


class ShipmentSerializer(serializers.ModelSerializer):

    class Meta:

        model = Shipment

        fields = (
            "id",
            "order",
            "status",
            "tracking_code",
            "shipped_at",
            "delivered_at",
            "created_at",
        )


        read_only_fields = (
            "id",
            "status",
            "shipped_at",
            "delivered_at",
            "created_at",
        )