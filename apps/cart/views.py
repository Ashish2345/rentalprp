import json
import requests
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from apps.core.utils import create_notification

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from .cart import Cart
from .forms import CheckoutForm
from .models import KhaltiPaymentLog

from apps.property.models import Property
from apps.booking.utilities import checkout, notify_landlord, notify_customer




@login_required
def cart_detail(request):
    cart = Cart(request)

    form = CheckoutForm()
    remove_from_cart = request.GET.get('remove_from_cart', '')

    if remove_from_cart:
        cart.remove(remove_from_cart)

        return redirect('cart')
    return render(request, 'cart/cart.html', {'form': form})

@login_required
def success(request):
    return render(request, 'cart/success.html')


def initiate_khalti_payment(request):

    def book_property(user_info, total_cost):
        first_name = user_info.get('first_name')
        last_name = user_info.get('last_name')
        email = user_info.get('email')
        phone = user_info.get('phone')
        address = user_info.get('address')
        zipcode = user_info.get('zipcode')
        place = user_info.get('place')
        booking, booking_items = checkout(request, first_name, last_name, email, address, zipcode, place, phone,
                             total_cost)


        return booking_items


    if request.method == 'POST':
        data = json.loads(request.body)
        user = data.get('user')
        amount = data.get('amount')
        product_id = data.get('product_id')


        scheme = request.scheme
        host = request.get_host()
        base_url = f"{scheme}://{host}"

        cart_details = []

        for item in Cart(request).items():
            property_id = item['id']
            quantity = item['quantity']
            propert = Property.objects.filter(id=property_id).first()

            cart_details.append(
                {
                    "identity": f"order_{str(property_id)}_{random.randint(9999, 9999999)}",
                    "name": propert.title or "",
                    "total_price": int(propert.price) * int(quantity) * 100,
                    "quantity": str(quantity),
                    "unit_price": 1
                 }

                )
        payload = {
            "return_url": f"{base_url}/cart/payment/success/",
            "website_url": base_url,
            "amount": amount,
            "purchase_order_id": product_id,
            "purchase_order_name": "Property Payment",
            "customer_info": {
                "name": f"{user.get('first_name')} {user.get('last_name')}",
                "email": user.get("email"),
                "phone": user.get("phone"),
                "address": user.get("address")
            },
            "product_details": cart_details,
        }

        headers = {
            "Authorization": "Key de4f5c2e706b48fbb5fd99c95e73b65b",  # Replace with your actual secret key
            "Content-Type": "application/json"
        }

        response = requests.post("https://a.khalti.com/api/v2/epayment/initiate/", json=payload, headers=headers)
        if response.status_code == 200:
            booked_property = book_property(user, int(amount))
            from django.utils import timezone
            khalti_log = KhaltiPaymentLog.objects.create(purchase_order_id=product_id, paid_at=timezone.now())
            khalti_log.booking_items.set(booked_property)
        return JsonResponse(response.json(), status=response.status_code)

@csrf_exempt
def verify_khalti_payment(request):
    if request.method == 'GET':
        cart = Cart(request)
        allowed_fields = [
            'pidx', 'transaction_id', 'total_amount',
            'mobile', 'status', 'purchase_order_id'
        ]
        data = {field: request.GET.get(field) for field in allowed_fields}
        try:
            data['total_amount'] = int(data['total_amount'])
            recorded_log = KhaltiPaymentLog.objects.get(purchase_order_id=data["purchase_order_id"])
            recorded_log.pidx = data["pidx"]
            recorded_log.transaction_id= data["transaction_id"]
            recorded_log.total_amount= data["total_amount"]
            recorded_log.mobile= data["mobile"]
            recorded_log.status= data["status"]
            recorded_log.save()
            for items in  recorded_log.booking_items.all():
                items.customer_paid = True
                items.save()
                propertry = items.property
                propertry.status = "sold"
                propertry.save()
            cart.clear()
            booking_itm = recorded_log.booking_items.first()
            bookingg= booking_itm.booking
            notify_landlord(bookingg)
            notify_customer(bookingg)
            create_notification(request.user, "Payment Completed",f"You have successfully paid for {recorded_log.total_amount} for the property .")
            return redirect('success')

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)
