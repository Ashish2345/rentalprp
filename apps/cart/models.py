# models.py

from django.db import models

from apps.booking.models import BookingItem

class KhaltiPaymentLog(models.Model):
    booking_items = models.ManyToManyField(BookingItem, verbose_name=("Booking Items"))
    pidx = models.CharField(max_length=100, null=True, blank=True)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
    total_amount = models.IntegerField(null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True)
    purchase_order_id = models.CharField(max_length=100, null=True, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.purchase_order_id} - {self.status}"

    class Meta:
        verbose_name = "Payment Log"
        verbose_name_plural = "Payment Logs"


