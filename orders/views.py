from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from .services import OrderService
from .serializers import OrderSerializer


class CreateOrderAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(self, request):

        try:

            order = OrderService.create_order(
                request.user
            )


        except ValueError as e:

            return Response(
                {
                    "error": str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )


        serializer = OrderSerializer(
            order
        )


        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )


