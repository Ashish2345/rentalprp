from django.db import models

from apps.property.models import Property
from apps.registration.models import Customer


class Booking(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.IntegerField(default=0)
    customer = models.ManyToManyField(Customer, related_name='bookings')


    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.first_name

class BookingItem(models.Model):
    booking = models.ForeignKey(Booking, related_name='items', on_delete=models.CASCADE)
    property = models.ForeignKey(Property, related_name='items', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='items', on_delete=models.CASCADE)
    customer_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.id

    def get_total_price(self):
        return self.price * self.quantity

    def get_payment_log(self):
        return self.khaltipaymentlog_set.order_by('paid_at').first()

