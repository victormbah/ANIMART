from django.contrib import admin
from .models import Product, ProductImage

class ProductImageInline(admin.TabularInline):  # or StackedInline if you prefer
    model = ProductImage
    extra = 1  # number of extra forms

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    prepopulated_fields = {'slug': ('name',)}
    list_display = ['name', 'price', 'stock', 'category', 'slug']

admin.site.register(Product, ProductAdmin)
