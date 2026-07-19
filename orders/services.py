from django.db import transaction

from .models import Order, OrderItem
from cart.models import Cart


class OrderService:


    @staticmethod
    @transaction.atomic
    def create_order(user):

        cart = Cart.objects.get(
            user=user
        )


        cart_items = cart.items.all()


        if not cart_items.exists():
            raise ValueError(
                "سبد خرید خالی است"
            )


        total_price = 0


        order = Order.objects.create(
            user=user
        )


        for item in cart_items:


            price = item.product.price


            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=price
            )


            total_price += price * item.quantity



        order.total_price = total_price

        order.save()


        cart_items.delete()


        return order