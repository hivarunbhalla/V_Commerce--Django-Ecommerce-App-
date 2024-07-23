from datetime import timezone
from django.db import models
from django.conf import settings
from ..base.models import BaseModel
from ..products.models import Product
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

# Cart
# CartItem
# Order
# OrderItem
# cOUPONS


class Cart(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # Allow guest user

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
    

class Coupon(BaseModel):
    DISCOUNT_TYPE_CHOICES = (
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
    )

    code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    discount_type = models.CharField(max_length=10, choices=DISCOUNT_TYPE_CHOICES, default='percentage')
    discount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)]
    )
    active = models.BooleanField(default=True)
    # customer_segments = models.ManyToManyField(CustomerSegment, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.code} - {self.get_discount_type_display()}: {self.discount}"

    def is_valid(self):
        now = timezone.now()
        return self.active and self.valid_from <= now <= self.valid_to

    def clean(self):
        if self.valid_from >= self.valid_to:
            raise ValidationError("'Valid from' date must be before 'Valid to' date.")
        
        if self.discount_type == 'percentage' and self.discount > 100:
            raise ValidationError("Percentage discount cannot be greater than 100%.")

    def apply_discount(self, order_total):
        if self.discount_type == 'percentage':
            return order_total * (1 - self.discount / 100)
        else:  # fixed amount
            return min(order_total - self.discount, order_total)  # Ensure discount doesn't exceed order total

    def get_discount_display(self):
        if self.discount_type == 'percentage':
            return f"{self.discount}%"
        else:
            return f"${self.discount:.2f}"
