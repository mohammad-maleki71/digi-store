from django.db import models
from django.conf import settings
from orders.models import Order


class ShippingAddress(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="addresses"
    )


    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="shipping_address"
    )


    full_name = models.CharField(
        max_length=255
    )


    phone = models.CharField(
        max_length=11
    )


    province = models.CharField(
        max_length=100
    )


    city = models.CharField(
        max_length=100
    )


    address = models.TextField()


    postal_code = models.CharField(
        max_length=10
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.full_name


class Shipment(models.Model):

    STATUS_CHOICES = (

        ("pending", "Pending"),

        ("packing", "Packing"),

        ("sent", "Sent"),

        ("delivered", "Delivered"),

    )


    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name="shipment"
    )


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )


    tracking_code = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )


    shipped_at = models.DateTimeField(
        blank=True,
        null=True
    )


    delivered_at = models.DateTimeField(
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
        return f"Shipment {self.id}"


