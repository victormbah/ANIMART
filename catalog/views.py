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
