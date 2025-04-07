from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, Category
from django.http import HttpResponse
from .forms import CheckoutForm

# Home Page: Display products
def home(request):
    products = Item.objects.all()
    return render(request, 'catalog/home.html', {
        'products': products
    })

# Cart Page: Display the current cart (using session)
def cart(request):
    cart = request.session.get('cart', {})
    total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())
    return render(request, 'catalog/cart.html', {
        'cart': cart,
        'total_price': total_price,
    })

# Add to Cart: Add a product to the session-based cart
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    cart = request.session.get('cart', {})

    if slug in cart:
        cart[slug]['quantity'] += 1
    else:
        cart[slug] = {
            'name': item.name,
            'price': str(item.price),
            'quantity': 1,
            'slug': slug,
        }

    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')

# Checkout Page: Display checkout form
def checkout(request):
    cart = request.session.get('cart', {})
    total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())
    form = CheckoutForm()

    if request.method == 'POST' and form.is_valid():
        shipping_address = form.cleaned_data['shipping_address']
        phone_number = form.cleaned_data['phone_number']
        email = form.cleaned_data['email']
        payment_method = form.cleaned_data['payment_method']
        return redirect('order_confirmation')

    return render(request, 'catalog/checkout.html', {
        'cart': cart,
        'total_price': total_price,
        'form': form,
    })

# Shop Page: Display all products with filtering and sorting options
def shop(request):
    products = Item.objects.all()
    categories = Category.objects.all()  # Get all categories for filter
    category_slug = request.GET.get('category')
    sort_by = request.GET.get('sort_by')

    if category_slug:
        products = products.filter(category__slug=category_slug)

    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')

    return render(request, 'catalog/shop.html', {
        'products': products,
        'categories': categories,
    })

# Contact Page: Display a contact form
def contact(request):
    return render(request, 'catalog/contact.html')

# Order Confirmation Page: Display a success message after order is placed
def order_confirmation(request):
    return render(request, 'catalog/order_confirmation.html')

# Update Cart: Update the quantity of a product in the cart
def update_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    cart = request.session.get('cart', {})
    action = request.GET.get('action')

    if slug in cart:
        if action == 'increase':
            cart[slug]['quantity'] += 1
        elif action == 'decrease' and cart[slug]['quantity'] > 1:
            cart[slug]['quantity'] -= 1
        elif action == 'decrease' and cart[slug]['quantity'] == 1:
            del cart[slug]
    
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')

# Remove from Cart: Remove an item from the cart
def remove_from_cart(request, slug):
    cart = request.session.get('cart', {})
    if slug in cart:
        del cart[slug]
    
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')

# Category List Page: Display all categories
def category_list(request):
    categories = Category.objects.all()  # Get all categories
    return render(request, 'catalog/category_list.html', {
        'categories': categories
    })




