from django.db import models


class Coupon(models.Model):

    code = models.CharField(
        max_length=50,
        unique=True
    )


    discount_percent = models.PositiveIntegerField()


    is_active = models.BooleanField(
        default=True
    )


    start_date = models.DateTimeField(
        null=True,
        blank=True
    )


    end_date = models.DateTimeField(
        null=True,
        blank=True
    )


    usage_limit = models.PositiveIntegerField(
        null=True,
        blank=True
    )


    used_count = models.PositiveIntegerField(
        default=0
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.code