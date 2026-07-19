from rest_framework import serializers

from .models import Inventory


class InventorySerializer(serializers.ModelSerializer):

    product_title = serializers.CharField(
        source="product.title",
        read_only=True
    )

    class Meta:
        model = Inventory

        fields = (
            "id",
            "product",
            "product_title",
            "quantity",
            "is_available",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "product_title",
            "updated_at",
        )