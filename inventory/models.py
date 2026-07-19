from django.db import models

from products.models import Product


class Inventory(models.Model):

    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        related_name="inventory"
    )


    quantity = models.PositiveIntegerField(
        default=0
    )


    is_available = models.BooleanField(
        default=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):
        return self.product.title


