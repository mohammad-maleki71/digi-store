from django.db import transaction

from .models import Order, OrderItem

from inventory.services import InventoryService
from coupons.services import CouponService



class OrderService:


    @staticmethod
    @transaction.atomic
    def create_order(
        user,
        cart,
        coupon_code=None
    ):


        total_price = 0

        for item in cart.items.all():

            total_price += (
                item.product.price *
                item.quantity
            )

        discount = 0
        coupon = None

        if coupon_code:

            result = CouponService.apply_coupon(
                coupon_code,
                total_price
            )

            coupon = result["coupon"]

            discount = result["discount"]

            total_price = result["final_price"]

        order = Order.objects.create(

            user=user,

            total_price=total_price,

            discount=discount,

            coupon=coupon,

            status="pending"

        )

        for item in cart.items.all():


            InventoryService.decrease_stock(

                item.product,

                item.quantity

            )

            OrderItem.objects.create(

                order=order,

                product=item.product,

                quantity=item.quantity,

                price=item.product.price

            )

        cart.items.all().delete()

        return order