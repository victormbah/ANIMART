from django.contrib import admin
from .models import Item, Order, OrderItem

class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # Automatically generates the slug from the name
    list_display = ['name', 'price', 'discount_price', 'slug']  # Include 'discount_price' in the list

# Registering models with the admin
admin.site.register(Item, ItemAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
