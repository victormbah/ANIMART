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
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('ajax_add_to_cart/<int:product_id>/', views.ajax_add_to_cart, name='ajax_add_to_cart'),
    path('payment/start/', views.start_payment, name='start_payment'),
    path('payment/verify/', views.verify_payment, name='verify_payment'),
    path('catalog/search/', views.search_products, name='search_products'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service_view, name='terms_of_service'),
]
