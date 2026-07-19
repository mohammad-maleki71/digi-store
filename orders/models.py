from django.db import models
from django.conf import settings


class Order(models.Model):

    STATUS_CHOICES = (

        ("pending", "Pending"),

        ("paid", "Paid"),

        ("cancelled", "Cancelled"),

    )


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )


    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=0,
        default=0
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):
        return f"Order {self.id}"


class OrderItem(models.Model):

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items"
    )


    product = models.ForeignKey(
        "products.Product",
        on_delete=models.PROTECT
    )


    quantity = models.PositiveIntegerField(
        default=1
    )


    price = models.DecimalField(
        max_digits=12,
        decimal_places=0
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.product.title


