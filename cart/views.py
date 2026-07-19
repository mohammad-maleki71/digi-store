from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CartSerializer
from rest_framework import status
from .serializers import AddToCartSerializer
from products.models import Product
from .models import Cart, CartItem
from .serializers import UpdateCartItemSerializer


class CartAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def get(self, request):

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        serializer = CartSerializer(cart)

        return Response(
            serializer.data
        )


class AddToCartAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(self, request):

        serializer = AddToCartSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )


        product_id = serializer.validated_data["product_id"]

        quantity = serializer.validated_data["quantity"]


        cart, created = Cart.objects.get_or_create(
            user=request.user
        )


        product = Product.objects.get(
            id=product_id
        )


        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product
        )


        if not created:
            cart_item.quantity += quantity

        else:
            cart_item.quantity = quantity


        cart_item.save()


        return Response(
            {
                "message": "product added to cart successfully",
            },
            status=status.HTTP_201_CREATED
        )


class UpdateCartItemAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def patch(self, request, pk):

        serializer = UpdateCartItemSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )


        try:
            cart_item = CartItem.objects.get(
                id=pk,
                cart__user=request.user
            )

        except CartItem.DoesNotExist:
            return Response(
                {
                    "error": "آیتم پیدا نشد"
                },
                status=status.HTTP_404_NOT_FOUND
            )


        cart_item.quantity = serializer.validated_data["quantity"]

        cart_item.save()


        return Response(
            {
                "message": "quantity updated successfully",
            }
        )


class RemoveCartItemAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def delete(self, request, pk):

        try:
            cart_item = CartItem.objects.get(
                id=pk,
                cart__user=request.user
            )

        except CartItem.DoesNotExist:
            return Response(
                {
                    "error": "item not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )


        cart_item.delete()


        return Response(
            {
                "message": "product removed successfully",
            },
            status=status.HTTP_204_NO_CONTENT
        )




