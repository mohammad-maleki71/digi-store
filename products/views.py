from rest_framework.viewsets import ModelViewSet
from .models import Category, Brand, Product, ProductImage
from .serializers import CategorySerializer, BrandSerializer, ProductSerializer, ProductImageSerializer


class CategoryViewSet(ModelViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BrandViewSet(ModelViewSet):

    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ProductViewSet(ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductImageViewSet(ModelViewSet):

    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer







