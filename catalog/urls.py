from django.urls import path
from . import views

urlpatterns = [
    # Home page
    path('', views.home, name='home'),

    # Cart page
    path('cart/', views.cart, name='cart'),

    # Update cart quantity
    path('cart/update/<slug:slug>/', views.update_cart, name='update_cart'),

    # Remove item from cart
    path('cart/remove/<slug:slug>/', views.remove_from_cart, name='remove_from_cart'),

    # Add to cart
    path('add_to_cart/<slug:slug>/', views.add_to_cart, name='add_to_cart'),

    # Checkout page
    path('checkout/', views.checkout, name='checkout'),

    # Shop page
    path('shop/', views.shop, name='shop'),

    # Contact page
    path('contact/', views.contact, name='contact'),

    # Order confirmation page
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
]
