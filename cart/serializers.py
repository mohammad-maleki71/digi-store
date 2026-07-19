from rest_framework import serializers
from products.models import Product
from .models import Cart, CartItem
from products.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):

    product = ProductSerializer(
        read_only=True
    )

    class Meta:
        model = CartItem

        fields = (
            "id",
            "product",
            "quantity",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )


class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerializer(
        many=True,
        read_only=True
    )

    total_price = serializers.SerializerMethodField()


    class Meta:
        model = Cart

        fields = (
            "id",
            "items",
            "total_price",
            "created_at",
            "updated_at",
        )


    def get_total_price(self, obj):

        total = 0

        for item in obj.items.all():

            total += item.product.price * item.quantity

        return total


class AddToCartSerializer(serializers.Serializer):

    product_id = serializers.IntegerField()

    quantity = serializers.IntegerField(
        min_value=1
    )

    def validate_product_id(self, value):

        try:
            Product.objects.get(
                id=value,
                is_active=True
            )

        except Product.DoesNotExist:
            raise serializers.ValidationError(
                "product not found"
            )

        return value


class UpdateCartItemSerializer(serializers.Serializer):

    quantity = serializers.IntegerField(
        min_value=1
    )