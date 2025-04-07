from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils.text import slugify

# Choices for order status
ORDER_STATUS = [
    ('pending', 'Pending'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('completed', 'Completed'),
]

# Item model represents a product in the catalog
class Item(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)  # Allow slug to be blank initially
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        # Automatically generate a slug if it's empty
        if not self.slug:
            self.slug = slugify(self.name)
        super(Item, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


# OrderItem model represents an individual item within an order
class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='catalog_orderitems')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='catalog_orderitems')
    ordered = models.BooleanField(default=False)  # If the item has been ordered
    quantity = models.IntegerField(default=1)  # Quantity of this item in the order

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"


# Order model represents a customer's entire order
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='catalog_orders')
    items = models.ManyToManyField(OrderItem)  # Multiple items can belong to an order
    ordered = models.BooleanField(default=False)  # If the order has been placed
    order_number = models.CharField(max_length=255, unique=True)  # Unique order number
    start_date = models.DateTimeField(auto_now_add=True)  # Date when the order was created
    ordered_date = models.DateTimeField(null=True, blank=True)  # Date when the order was completed
    status = models.CharField(max_length=20, choices=ORDER_STATUS, default='pending')  # Order status (pending, paid, etc.)

    def __str__(self):
        return f"Order {self.order_number} by {self.user.username}"

    # Override save method to generate a unique order number
    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = str(uuid.uuid4())  # Generate a unique order number using UUID
        super(Order, self).save(*args, **kwargs)
