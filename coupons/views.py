from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Coupon
from .serializers import CouponSerializer
from .serializers import ApplyCouponSerializer
from .services import CouponService


class CouponViewSet(ModelViewSet):

    queryset = Coupon.objects.all()

    serializer_class = CouponSerializer


class ApplyCouponAPIView(APIView):

    permission_classes = [
        IsAuthenticated
    ]


    def post(self, request):

        serializer = ApplyCouponSerializer(
            data=request.data
        )


        serializer.is_valid(
            raise_exception=True
        )


        result = CouponService.apply_coupon(
            serializer.validated_data["code"],
            serializer.validated_data["cart_total"]
        )


        return Response(
            {
                "code": result["coupon"].code,
                "discount": result["discount"],
                "final_price": result["final_price"]
            }
        )