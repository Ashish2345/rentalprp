from django.conf import settings
from django.shortcuts import render, HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib import messages

from .models import Notification
from django.shortcuts import get_object_or_404


# Create your views here.
def homepage(request):
    return render(request, 'core/homePage.html')

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']

        full_message = f"""
            You have a new contact form submission.

            Name: {name}
            Email: {email}
            Phone: {phone}

            Message:
            {message}
            """

        # send email
        send_mail(
            'Message from ' + name,
            full_message,
            settings.DEFAULT_FROM_EMAIL,
            [email],
        )
        messages.success(request, 'Thank you for contacting us! We have received your message and will get back to you shortly.')
        if request.GET.get("page"):
            return render(request, 'core/homePage.html')

        return render(request, 'core/contact.html', {'name': name})
    return render(request, 'core/contact.html')



def about(request):
    return render(request, 'core/about.html')


def view_notifications(request, id):
    # Get the notification by its ID
    notification = get_object_or_404(Notification, id=id)

    # Mark the notification as viewed
    notification.viewed = True
    notification.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))