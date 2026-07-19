from rest_framework.viewsets import ModelViewSet

from .models import Inventory
from .serializers import InventorySerializer


class InventoryViewSet(ModelViewSet):

    queryset = Inventory.objects.all()

    serializer_class = InventorySerializer