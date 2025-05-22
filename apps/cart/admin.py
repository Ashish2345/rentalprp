from django.contrib import admin
from .models import KhaltiPaymentLog, BookingItem

class KhaltiPaymentLogAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'status',
        'paid_at',
        'total_amount',
        'get_property_names',
        'get_customer_usernames',
    )
    search_fields = ('status', 'pidx', 'transaction_id', 'purchase_order_id', 'mobile')
    list_filter = ('status', 'paid_at')
    readonly_fields = ('paid_at',)

    def get_property_names(self, obj):
        properties = obj.booking_items.select_related('property').all()
        return ", ".join(set(item.property.title for item in properties))
    get_property_names.short_description = "Properties"

    def get_customer_usernames(self, obj):
        customers = obj.booking_items.select_related('customer__created_by').all()
        return ", ".join(set(item.customer.created_by.username for item in customers))
    get_customer_usernames.short_description = "Customers"

admin.site.register(KhaltiPaymentLog, KhaltiPaymentLogAdmin)
