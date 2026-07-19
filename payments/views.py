from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .services import PaymentService
from .serializers import PaymentSerializer


class CreatePaymentAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(self, request):

        order_id = request.data.get(
            "order_id"
        )


        payment = PaymentService.create_payment(
            request.user,
            order_id
        )


        serializer = PaymentSerializer(
            payment
        )


        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class VerifyPaymentAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(self, request):

        payment_id = request.data.get(
            "payment_id"
        )


        payment = PaymentService.verify_payment(
            payment_id,
            request.user
        )


        serializer = PaymentSerializer(
            payment
        )


        return Response(
            serializer.data
        )