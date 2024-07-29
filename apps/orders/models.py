from django.utils import timezone
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal

from apps.promotions.models import Coupon
from ..base.models import BaseModel
from ..products.models import Product, ProductVariant

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
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
    @property
    def total_price(self):
        return self.quantity * self.variant.varient_price

    def __str__(self):
        return f"{self.quantity} of {self.product.sku} in Cart {self.cart.uid}"

# class Order(BaseModel):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)  # Allow guest users
#     status = models.CharField(max_length=50, default='Pending')  # e.g., 'Pending', 'Completed', 'Cancelled'
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     shipping_address = models.TextField()
#     billing_address = models.TextField(blank=True, null=True)  # Optional

#     def __str__(self):
#         return f"Order {self.uid} for {self.user or 'Guest'}"

# class OrderItem(BaseModel):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     price = models.DecimalField(max_digits=10, decimal_places=2)  # Store price at the time of order

#     def __str__(self):
#         return f"{self.quantity} of {self.product.name} in Order {self.order.uid}"
    


class Order(BaseModel):
    STATUS_CHOICES = [
            ('PENDING', 'Pending'), 
            ('PROCESSING', 'Processing'),
            ('SHIPPED', 'Shipped'),
            ('DELIVERED', 'Delivered'),
            ('CANCELLED', 'Cancelled'),
        ]
    STATUS_DEFAULT = 'PENDING'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default=STATUS_DEFAULT
    )
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    shipping_address = models.TextField()
    billing_address = models.TextField(blank=True, null=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True, related_name='orders')
    discount_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.uid} for {self.user.username if self.user else 'Guest'}"

    class Meta:
        ordering = ['-created_at']

    @property
    def total_items(self):
        return self.orderitems.count()

    @property
    def subtotal(self):
        return sum(item.subtotal for item in self.orderitems.all())

    @property
    def discounted_total(self):
        return max(self.subtotal - self.discount_amount, Decimal('0.00'))

    def apply_coupon(self):
        if self.coupon and self.coupon.is_valid():
            if self.subtotal >= self.coupon.minimum_amount:
                self.discount_amount = self.coupon.apply_discount(self.subtotal)
                self.save()
                return True
        return False

    def remove_coupon(self):
        self.coupon = None
        self.discount_amount = Decimal('0.00')
        self.save()

    def save(self, *args, **kwargs):
        if self.coupon:
            self.apply_coupon()
        super().save(*args, **kwargs)


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    # variations = models.ManyToManyField(Variation, blank=True)
    product_name = models.CharField(max_length=255)
    product_sku = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )

    def __str__(self):
        return f"{self.quantity} of {self.product_sku} in Order {self.order.uid}"

    class Meta:
        unique_together = ['order', 'product']

    @property
    def subtotal(self):
        return self.quantity * self.price

    def save(self, *args, **kwargs):
        if self.product:
            self.product_name = self.product.product_title
            self.product_sku = self.product.sku
        super().save(*args, **kwargs)

