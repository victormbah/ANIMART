from django.shortcuts import render, get_object_or_404, redirect
from .models import Item
from django.http import HttpResponse

# Home Page: Display products
def home(request):
    products = Item.objects.all()
    return render(request, 'catalog/home.html', {
        'products': products
    })

# Cart Page: Display the current cart (using session)
def cart(request):
    cart = request.session.get('cart', {})  # Retrieve cart from session
    total_price = sum(float(item['price']) * item['quantity'] for item in cart.values())
    return render(request, 'catalog/cart.html', {
        'cart': cart,
        'total_price': total_price,
    })

# Add to Cart: Add a product to the session-based cart
def add_to_cart(request, slug):
    # Fetch the item using the slug from the database
    item = get_object_or_404(Item, slug=slug)
    
    # Get the current cart from the session or initialize an empty cart
    cart = request.session.get('cart', {})

    # Check if the item is already in the cart
    if slug in cart:
        # If the item is in the cart, increment the quantity by 1
        cart[slug]['quantity'] += 1
    else:
        # If the item is not in the cart, add it with quantity 1
        cart[slug] = {
            'name': item.name,
            'price': str(item.price),  # Store price as a string to avoid floating point issues
            'quantity': 1,  # Start with a quantity of 1
            'slug': slug,  # Store the slug for reference
        }

    # Save the updated cart in the session
    request.session['cart'] = cart
    request.session.modified = True

    # Redirect the user to the cart page after adding the item
    return redirect('cart')

# Checkout Page: Display checkout form
def checkout(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0

    for slug, item in cart.items():
        cart_items.append(item)
        total_price += float(item['price']) * item['quantity']

    if request.method == 'POST':
        shipping_address = request.POST.get('shipping_address')
        payment_method = request.POST.get('payment_method')
        # Process the order here (e.g., save order, integrate payment, etc.)
        return redirect('order_confirmation')

    return render(request, 'catalog/checkout.html', {
        'cart': cart,
        'total_price': total_price,
        'cart_items': cart_items,
    })

# Shop Page: Display all products
def shop(request):
    products = Item.objects.all()
    return render(request, 'catalog/shop.html', {
        'products': products
    })

# Contact Page: Display a contact form
def contact(request):
    return render(request, 'catalog/contact.html')

# Order Confirmation Page: Display a success message after order is placed
def order_confirmation(request):
    return render(request, 'catalog/order_confirmation.html')

# Update Cart: Update the quantity of a product in the cart
def update_cart(request, slug):
    # Get the item by its slug
    item = get_object_or_404(Item, slug=slug)
    
    # Get the current cart from session
    cart = request.session.get('cart', {})
    
    # Get the action ('increase' or 'decrease') from the request
    action = request.GET.get('action')  # Action will be passed from the button click (e.g., increase or decrease)
    
    if slug in cart:
        if action == 'increase':
            cart[slug]['quantity'] += 1  # Increase quantity by 1
        elif action == 'decrease' and cart[slug]['quantity'] > 1:
            cart[slug]['quantity'] -= 1  # Decrease quantity by 1
        elif action == 'decrease' and cart[slug]['quantity'] == 1:
            del cart[slug]  # If quantity is 1 and decrease is clicked, remove the item from the cart
    
    # Save the updated cart to session
    request.session['cart'] = cart
    request.session.modified = True

    # Redirect to the cart page
    return redirect('cart')


# Remove from Cart: Remove an item from the cart
def remove_from_cart(request, slug):
    # Get the item by its slug
    item = get_object_or_404(Item, slug=slug)
    
    # Get the current cart from the session
    cart = request.session.get('cart', {})

    # Check if the item exists in the cart
    if slug in cart:
        # Remove the item from the cart
        del cart[slug]
        
        # Save the updated cart back to the session
        request.session['cart'] = cart
        request.session.modified = True

    # Redirect to the cart page or another relevant page
    return redirect('cart')
