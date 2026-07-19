from django.db import transaction
from orders.models import Order
from .models import Payment


class PaymentService:


    @staticmethod
    @transaction.atomic
    def verify_payment(payment_id, user):

        payment = Payment.objects.select_for_update().get(
            id=payment_id,
            order__user=user
        )

        gateway_result = True

        if gateway_result:

            payment.status = "success"

            payment.transaction_id = "TEST123456"

            payment.save()


            order = payment.order

            order.status = "paid"

            order.save()


        else:

            payment.status = "failed"

            payment.save()


        return payment