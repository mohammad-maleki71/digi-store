from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from orders.models import Order
from .models import ShippingAddress
from .serializers import ShippingAddressSerializer
from .models import Shipment
from .serializers import ShipmentSerializer


class CreateShippingAddressAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(self, request):

        order_id = request.data.get(
            "order"
        )


        order = Order.objects.get(
            id=order_id,
            user=request.user
        )


        serializer = ShippingAddressSerializer(
            data=request.data
        )


        serializer.is_valid(
            raise_exception=True
        )


        serializer.save(
            user=request.user,
            order=order
        )


        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


class ShipmentDetailAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request, order_id):

        shipment = Shipment.objects.get(
            order__id=order_id,
            order__user=request.user
        )


        serializer = ShipmentSerializer(
            shipment
        )


        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )