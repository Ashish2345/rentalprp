from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.property.models import Property


@login_required
def frontpage(request):
    newest_property = Property.objects.exclude(items__customer_paid=True).distinct()[:8]
    return render(request, 'home/frontPage.html', {'newest_property': newest_property})


from django.shortcuts import render

def property_list(request):
    # Get the currently logged-in user
    user = request.user

    # Ensure the user is authenticated (if needed)
    if user.is_authenticated:
        # Exclude properties posted by the logged-in user
        newest_property = Property.objects.exclude(user=user).order_by('-created_at')
    else:
        # If not logged in, show all properties
        newest_property = Property.objects.all().order_by('-created_at')

    return render(request, 'property/property_list.html', {'newest_property': newest_property})
