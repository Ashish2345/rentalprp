from django.contrib import admin
from django.utils.html import format_html

# Register your models here.
from .models import Booking, BookingItem

class BookingAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'place', 'phone')
    search_fields = ['first_name', 'phone', 'place']

class BookingItemAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'get_property_title',
        'get_property_image',
        'get_property_category',
        'get_customer_email',
        'get_booking_info',
        'customer_paid',
        'get_paid_status',
        'price',
    )
    list_filter = ('customer_paid', 'property__category')
    search_fields = ('property__title', 'property__category__title', 'booking__place')

    def get_property_title(self, obj):
        return obj.property.title
    get_property_title.short_description = 'Property'

    def get_property_image(self, obj):
        if hasattr(obj.property, 'get_thumbnail') and obj.property.get_thumbnail:
            return format_html(
                '<img src="{}" style="height:60px; width:90px; object-fit:cover; border-radius:6px;" />',
                obj.property.get_thumbnail()
            )
        return 'No Image'
    get_property_image.short_description = 'Image'

    def get_property_category(self, obj):
        return obj.property.category.title
    get_property_category.short_description = 'Category'

    def get_customer_email(self, obj):
        return obj.customer.created_by.email
    get_customer_email.short_description = 'Customer Email'

    def get_paid_status(self, obj):
        return obj.get_payment_log().status
    get_paid_status.short_description = 'Payment Status'

    def get_booking_info(self, obj):
        return f"{obj.booking.first_name} {obj.booking.last_name} ({obj.booking.phone})"
    get_booking_info.short_description = 'Booking Info'


admin.site.register(Booking, BookingAdmin)
admin.site.register(BookingItem, BookingItemAdmin)
