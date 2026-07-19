from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from orders.models import Order

from .models import Payment
from .serializers import CreatePaymentSerializer
from .services import PaymentService



class CreatePaymentAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(self, request):

        serializer = CreatePaymentSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )


        order_id = serializer.validated_data["order_id"]


        order = Order.objects.get(
            id=order_id,
            user=request.user
        )


        payment = PaymentService.create_payment(
            order
        )


        return Response(
            {
                "payment_id": payment.id,
                "amount": payment.amount,
                "status": payment.status,
            }
        )


class VerifyPaymentAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request):

        payment_id = request.query_params.get(
            "payment_id"
        )


        transaction_id = request.query_params.get(
            "transaction_id"
        )


        payment = Payment.objects.get(
            id=payment_id,
            order__user=request.user
        )


        PaymentService.verify_payment(
            payment,
            transaction_id
        )


        return Response(
            {
                "message": "Payment successful"
            }
        )