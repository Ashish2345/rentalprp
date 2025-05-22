from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import BookingItem

# Create your views here.
@login_required
def orders(request):
    my_properties = BookingItem.objects.filter(customer=request.user.customer)
    return render(request, 'booking/my_bookings.html', {'my_properties': my_properties})

