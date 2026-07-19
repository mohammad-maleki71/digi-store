from django.db import transaction

from .models import Payment

from orders.models import Order


class PaymentService:


    @staticmethod
    @transaction.atomic
    def create_payment(order):

        payment = Payment.objects.create(

            order=order,

            amount=order.total_price,

            status="pending"

        )


        # اینجا بعداً اتصال به درگاه قرار می‌گیرد
        # مثلا:
        #
        # authority = gateway.request(
        #     amount=payment.amount
        # )
        #
        # payment.authority = authority


        payment.save()


        return payment



    @staticmethod
    @transaction.atomic
    def verify_payment(
        payment,
        transaction_id
    ):


        # اینجا بعداً پاسخ واقعی درگاه بررسی می‌شود


        payment.status = "success"

        payment.transaction_id = transaction_id

        payment.save()



        order = payment.order


        order.status = "paid"

        order.save()



        # افزایش تعداد استفاده از کوپن
        if order.coupon:

            coupon = order.coupon

            coupon.used_count += 1

            coupon.save()



        return payment