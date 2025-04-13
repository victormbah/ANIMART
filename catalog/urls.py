from django.urls import path
from . import views
from .views import view_cart

urlpatterns = [
    path('', views.home, name='home'),
    path('cart/', view_cart, name='view_cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('update_cart/<int:product_id>/', views.update_cart, name='update_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),    # Use the built-in LogoutView
    path('profile/', views.profile, name='profile'),
    path('ajax_add_to_cart/<int:product_id>/', views.ajax_add_to_cart, name='ajax_add_to_cart'),
]
