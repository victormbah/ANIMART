from django.contrib import admin
from .models import Product
# from .models import Order, OrderItem

class ItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}  # Automatically generates the slug from the name
    list_display = ['name', 'price', 'discount_price', 'slug']  # Include 'discount_price' in the list

# Registering models with the admin
admin.site.register(Product)

 