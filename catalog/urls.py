from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<slug:slug>/', views.add_to_cart, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('shop/', views.shop, name='shop'),
    path('contact/', views.contact, name='contact'),
    path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
    path('update_cart/<slug:slug>/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<slug:slug>/', views.remove_from_cart, name='remove_from_cart'),
    path('categories/', views.category_list, name='category_list'),  # New path for categories list
]
