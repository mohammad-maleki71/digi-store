from rest_framework import serializers
from .models import (
    Category,
    Brand,
    Product,
    ProductImage,
)


class ParentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "title",
            "slug",
        )


class CategorySerializer(serializers.ModelSerializer):
    parent = ParentCategorySerializer(read_only=True)

    class Meta:
        model = Category
        fields = (
            "id",
            "title",
            "slug",
            "parent",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "slug",
            "created_at",
            "updated_at",
        )


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = (
            "id",
            "image",
            "alt",
            "is_main",
        )


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            "id",
            "name",
            "slug",
            "logo",
        )


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)
    images = ProductImageSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Product
        fields = (
            "id",
            "category",
            "brand",
            "title",
            "slug",
            "description",
            "price",
            "images",
            "is_active",
            "created_at",
            "updated_at",
        )



