from django.db import models

from orders.models import Order


class Payment(models.Model):

    STATUS_CHOICES = (

        ("pending", "Pending"),

        ("success", "Success"),

        ("failed", "Failed"),

    )


    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="payment"
    )


    amount = models.DecimalField(
        max_digits=12,
        decimal_places=0
    )


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )


    transaction_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):
        return f"Payment {self.id}"


