from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import Product, Order, OrderItem
from django.template.loader import get_template
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
import requests
from django.conf import settings
from .models import Product
from django.db.models import Q

# Home Page
def home(request):
    products = Product.objects.all()
    return render(request, 'catalog/home.html', {'products': products})

# Register Page
def register(request):
    return render(request, 'catalog/register.html')

# User Login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Invalid login credentials', status=400)
    else:
        form = AuthenticationForm()
    return render(request, 'catalog/login.html', {'form': form})

# User Logout
@require_POST
def user_logout(request):
    logout(request)  # Logs out the user
    return redirect('home')

# Profile Page (currently redirects to home)
@login_required
def profile(request):
    return render(request, 'catalog/home.html')

# Add to Cart
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})

    product_id_str = str(product.id)
    cart[product_id_str] = cart.get(product_id_str, 0) + 1

    request.session['cart'] = cart
    return redirect('view_cart')

# Remove from Cart
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]

    request.session['cart'] = cart
    return redirect('view_cart')

# View Cart
def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            subtotal = product.price * quantity
            total_price += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
        except Product.DoesNotExist:
            continue

    return render(request, 'catalog/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'cart': cart,
    })

# Update Cart Quantity (Increase/Decrease)
@csrf_exempt
def update_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        action = request.POST.get('action')
        if action == 'increase':
            cart[product_id_str] += 1
        elif action == 'decrease':
            cart[product_id_str] -= 1
            if cart[product_id_str] <= 0:
                del cart[product_id_str]

    request.session['cart'] = cart
    return redirect('view_cart')

# Checkout Page
@login_required
def checkout(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        try:
            product = Product.objects.get(id=int(product_id))
            subtotal = product.price * quantity
            total_price += subtotal
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal
            })
        except Product.DoesNotExist:
            continue

    return render(request, 'catalog/checkout.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

# Place Order
@login_required
def place_order(request):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('view_cart')

        shipping_address = request.POST.get('shipping_address')
        payment_method = request.POST.get('payment_method')

        order = Order.objects.create(
            user=request.user,
            shipping_address=shipping_address,
            payment_method=payment_method
        )

        for product_id, quantity in cart.items():  # ✅ quantity is int
            product = get_object_or_404(Product, id=int(product_id))
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

        request.session['cart'] = {}

        return redirect('order_confirmation', order_id=order.id)

    return redirect('view_cart')

# Order Confirmation
@login_required
def order_confirmation(request, order_id):
    print(get_template('catalog/order_confirmation.html'))  # Debugging
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'catalog/order_confirmation.html', {'order': order})

# AJAX Add to Cart (optional use for dynamic frontend)
def ajax_add_to_cart(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    cart = request.session.get('cart', {})
    product_id_str = str(product.id)
    cart[product_id_str] = cart.get(product_id_str, 0) + 1

    request.session['cart'] = cart
    return JsonResponse({
        'cart_count': sum(cart.values())
    })
@login_required
def start_payment(request):
    if request.method == "POST":
        email = request.user.email

        # 🛒 Get cart from session
        cart = request.session.get('cart', {})
        cart_total = 0

        for product_id, quantity in cart.items():
            try:
                product = Product.objects.get(id=int(product_id))
                cart_total += product.price * quantity
            except Product.DoesNotExist:
                continue

        # ✅ Convert to kobo
        amount = int(cart_total * 100)

        # Store shipping address and payment method in session
        request.session['shipping_address'] = request.POST.get('shipping_address')
        request.session['payment_method'] = request.POST.get('payment_method')

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }

        data = {
            "email": email,
            "amount": amount,
            "callback_url": "http://127.0.0.1:8000/payment/verify/",  # Update to live domain later
        }

        response = requests.post(
            'https://api.paystack.co/transaction/initialize',
            json=data,
            headers=headers
        )
        res_data = response.json()

        if res_data.get('status'):
            auth_url = res_data['data']['authorization_url']
            return redirect(auth_url)
        else:
            return HttpResponse("Something went wrong during payment initialization")

    return redirect('checkout')


def verify_payment(request):
    ref = request.GET.get('reference')

    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
    }

    response = requests.get(f"https://api.paystack.co/transaction/verify/{ref}", headers=headers)
    res_data = response.json()

    if res_data['status'] and res_data['data']['status'] == 'success':
        # Mark order as paid or create a Payment model entry
        return render(request, 'catalog/payment_success.html', {'payment_data': res_data['data']})
    else:
        return render(request, 'catalog/payment_failed.html')

def search_products(request):
    query = request.GET.get('query', '')
    if query:
        results = Product.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    else:
        results = Product.objects.all()  # If no query, show all products
    
    return render(request, 'catalog/search_results.html', {
        'results': results,
        'query': query
    })

def privacy_policy_view(request):
    return render(request, 'catalog/privacy_policy.html')

def terms_of_service_view(request):
    return render(request, 'catalog/terms_of_service.html')
