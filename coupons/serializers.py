from rest_framework import serializers

from .models import Coupon


class CouponSerializer(serializers.ModelSerializer):

    class Meta:
        model = Coupon

        fields = (
            "id",
            "code",
            "discount_percent",
            "is_active",
            "start_date",
            "end_date",
            "usage_limit",
            "used_count",
            "created_at",
        )

        read_only_fields = (
            "id",
            "used_count",
            "created_at",
        )


class ApplyCouponSerializer(serializers.Serializer):

    code = serializers.CharField()

    cart_total = serializers.DecimalField(
        max_digits=12,
        decimal_places=0
    )


