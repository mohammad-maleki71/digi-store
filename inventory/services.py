from django.db import transaction

from .models import Inventory


class InventoryService:


    @staticmethod
    @transaction.atomic
    def decrease_stock(product, quantity):

        inventory = Inventory.objects.select_for_update().get(
            product=product
        )


        if inventory.quantity < quantity:
            raise ValueError(
                "Not enough stock"
            )


        inventory.quantity -= quantity


        if inventory.quantity == 0:
            inventory.is_available = False


        inventory.save()


        return inventory


    @staticmethod
    @transaction.atomic
    def increase_stock(product, quantity):

        inventory = Inventory.objects.get(
            product=product
        )


        inventory.quantity += quantity


        inventory.is_available = True


        inventory.save()


        return inventory


