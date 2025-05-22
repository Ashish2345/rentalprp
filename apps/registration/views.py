
from .forms import PropertyForm,CustomerForm,PropertyImageForm
from django.conf import settings
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import CreateUserForm
from django.utils.text import slugify
from .models import Customer
from django.contrib.auth.decorators import login_required
from apps.property.models import Property
from .tokens import account_activation_token
from .forms import PropertyForm, PropertyImageForm
from django.core.mail import EmailMessage, send_mail
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# In registration/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Customer
from .tokens import account_activation_token
from django.contrib.auth.decorators import login_required
from django.db import transaction


from apps.core.utils import create_notification

# Create your views here.

def registerPage(request):
    form = CreateUserForm()

    def send_confirmation_email(user, request):
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        domain = request.get_host()

        context = {
            'domain': domain,
            'uid': uid,
            'token': token,
            'name': user.username,
        }

        subject = "Email Confirmation"
        from_email = settings.DEFAULT_FROM_EMAIL
        to = [user.email]
        html_content = render_to_string("email_confirmation.html", context)

        email = EmailMessage(subject, html_content, from_email, to)
        email.content_subtype = "html"
        email.send()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                user = form.save()
                Customer.objects.create(name=user.username, created_by=user)
                messages.success(request, 'Email Confimation send at email:' + user.email)
                send_confirmation_email(user, request)
                return redirect('login')
    else:
        form = CreateUserForm

    context = {'form': form}
    return render(request, 'registration/register.html', context)


def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and account_activation_token.check_token(user, token):
        customer = Customer.objects.get(created_by=user)
        customer.is_email_verified = True
        customer.save()
        messages.success(request, 'Email confirmed successfully. You can now log in.')
        return redirect('login')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('login')

def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is None:
            messages.info(request, 'Username or password is incorrect!')
            return render(request, 'registration/login.html')

        try:
            customer = Customer.objects.get(created_by=user)
            if not customer.is_email_verified:
                messages.info(request, 'Please verify your email. A verification link has been sent to your email.')
                return render(request, 'registration/login.html')
        except Customer.DoesNotExist:
            messages.error(request, 'Customer profile not found.')
            return render(request, 'registration/login.html')

        login(request, user)
        create_notification(user, "Login Successful","You have successfully logged in to your account")
        return redirect(request.POST.get('next', 'frontpage'))

    return render(request, 'registration/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')




@login_required
def profile(request):
    try:
        # Try to get the related Customer object
        customer = request.user.customer
    except Customer.DoesNotExist:
        # If the customer does not exist, handle the case
        messages.error(request, "Your profile has not been set up yet.")
        return redirect('create_profile')  # Redirect to profile creation page

    # Assuming `property` and `bookings` are related models to the Customer
    property = customer.property.all()
    bookings = customer.bookings.all()

    # Handle bookings logic
    for booking in bookings:
        booking.customer_amount = 0
        booking.customer_paid_amount = 0
        booking.fully_paid = True

        for item in booking.items.all():
            if item.customer == request.user.customer:
                if item.customer_paid:
                    booking.customer_paid_amount += item.get_total_price()
                else:
                    booking.customer_amount += item.get_total_price()
                    booking.fully_paid = False

    # Return the profile page with the customer data
    return render(request, 'registration/profile.html', {'customer': customer, 'property': property, 'bookings': bookings})


@login_required
def add_property(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)

        if form.is_valid():
            property = form.save(commit=False)
            property.customer = request.user.customer
            property.slug = slugify(property.title)

            # Extract latitude and longitude from the POST data
            latitude = request.POST.get('latitude', None)
            longitude = request.POST.get('longitude', None)

            # Save latitude and longitude to the Property model
            property.latitude = latitude
            property.longitude = longitude

            property.save()
            create_notification(request.user, "Propertry Added",f"You have added {property.title} property.")


            return redirect('profile')
    else:
        form = PropertyForm()

    return render(request, 'registration/addProperty.html', {'form': form})

@login_required
def create_profile(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            customer = form.save(commit=False)
            customer.user = request.user
            customer.save()
            return redirect('profile')  # Redirect to the profile page after creating the profile
    else:
        form = CustomerForm()

    return render(request, 'registration/create_profile.html', {'form': form})


def edit_property(request, pk):
    property_instance = Property.objects.get(pk=pk)

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_instance)

        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = PropertyForm(instance=property_instance)

    return render(request, 'registration/edit_property.html', {'form': form, 'property_instance': property_instance})



@login_required
def edit_customer(request):
    customer = request.user.customer

    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')

        if name:
            customer.created_by.email = email
            customer.created_by.save()

            customer.name = name
            customer.save()

            return redirect('profile')

    return render(request, 'registration/edit_profile.html', {'customer': customer})

