from django.contrib import admin

# Register your models here.
from .models import Category, Property
from django.contrib import admin
from .models import PropertyImage
from PIL import Image

class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ('property', 'display_thumbnail')
    readonly_fields = ('display_thumbnail',)

    def display_thumbnail(self, obj):
        return obj.get_thumbnail_html()

    display_thumbnail.short_description = 'Thumbnail Preview'

admin.site.register(PropertyImage, PropertyImageAdmin)



class PropertyAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'customer_name', 'price', 'status', 'date_added')
    list_filter = ('status', 'category', 'customer')
    search_fields = ('title', 'slug', 'description', 'customer__name', 'customer__email')
    readonly_fields = ('date_added',)

    def customer_name(self, obj):
        return obj.customer.name
    customer_name.short_description = 'Property Owner'

    # Optional: To better format Decimal price
    def formfield_for_dbfield(self, db_field, **kwargs):
        from django.forms import TextInput
        if db_field.name == 'price':
            kwargs['widget'] = TextInput(attrs={'size': '10'})
        return super().formfield_for_dbfield(db_field, **kwargs)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'ordering', 'property_count')
    search_fields = ('title', 'slug')
    ordering = ('ordering',)

    def property_count(self, obj):
        return obj.property.count()
    property_count.short_description = 'Total Properties'
admin.site.register(Property, PropertyAdmin)
