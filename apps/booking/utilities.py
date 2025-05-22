from django.conf import settings
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.template.loader import render_to_string
from apps.cart.cart import Cart
from .models import Booking, BookingItem

def checkout(request, first_name, last_name, email, address, zipcode, place, phone, amount):
    booking = Booking.objects.create(first_name=first_name, last_name=last_name, email=email, address=address,
                                 zipcode=zipcode, place=place, phone=phone, paid_amount=amount)
    booking_properties = []
    for item in Cart(request):
        booking_item = BookingItem.objects.create(booking=booking, property=item['property'], customer=request.user.customer,
                                 price=item['property'].price, quantity=item['quantity'])

        booking.customer.add(request.user.customer)
        booking_properties.append(booking_item)

    return booking, booking_properties


def notify_landlord(booking):
    from_email = settings.EMAIL_HOST_USER

    for customer in booking.customer.all():
        to_email = customer.created_by.email
        subject = 'New Booking'
        text_content = 'You have a new booking!'
        html_content = render_to_string('booking/email_notify_landlord.html', {'booking': booking, 'customer': customer})

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


def notify_customer(booking):
    from_email = settings.EMAIL_HOST_USER

    to_email = booking.email
    subject = 'Order confirmation'
    text_content = 'Thank you for the booking!'
    html_content = render_to_string('booking/email_notify_customer.html', {'booking': booking})

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()

