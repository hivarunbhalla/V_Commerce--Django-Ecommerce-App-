from datetime import timezone
from django.db import models
from django.conf import settings

from apps.promotions.models import Coupon
from ..base.models import BaseModel
from ..products.models import Product


# Cart
# CartItem
# Order
# OrderItem
# cOUPONS


class Cart(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # Allow guest user
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True, related_name='coupon')

    def __str__(self):
        return f"{self.uid}"

class CartItem(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    @property
    def total_price(self):
        return self.quantity * self.product.product_price

    def __str__(self):
        return f"{self.quantity} of {self.product.sku} in Cart {self.cart.uid}"

class Order(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # Allow guest users
    status = models.CharField(max_length=50, default='Pending')  # e.g., 'Pending', 'Completed', 'Cancelled'
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_address = models.TextField()
    billing_address = models.TextField(blank=True, null=True)  # Optional

    def __str__(self):
        return f"Order {self.uid} for {self.user or 'Guest'}"

class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Store price at the time of order

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in Order {self.order.uid}"
    


