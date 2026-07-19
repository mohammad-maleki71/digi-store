from django.utils import timezone

from .models import Coupon


class CouponService:


    @staticmethod
    def apply_coupon(code, cart_total):

        coupon = Coupon.objects.filter(
            code=code,
            is_active=True
        ).first()


        if not coupon:
            raise ValueError(
                "Invalid coupon"
            )


        now = timezone.now()


        if coupon.start_date and now < coupon.start_date:
            raise ValueError(
                "Coupon is not active yet"
            )


        if coupon.end_date and now > coupon.end_date:
            raise ValueError(
                "Coupon expired"
            )


        if (
            coupon.usage_limit
            and coupon.used_count >= coupon.usage_limit
        ):
            raise ValueError(
                "Coupon usage limit reached"
            )


        discount = (
            cart_total *
            coupon.discount_percent
            /
            100
        )


        final_price = cart_total - discount


        return {
            "coupon": coupon,
            "discount": discount,
            "final_price": final_price
        }