from django.db import models
from django.conf import settings
from ..base.models import BaseModel
from ..products.models import Product

# Cart
# CartItem
# Order
# OrderItem

class Cart(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL , on_delete=models.CASCADE, related_name='cart', null=True, blank=True)

    def __str__(self):
        return f"{self.uid}"

    def total_price(self):
        return sum(item.total_price() for item in self.cart_items.all())

class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.uid}"

    def total_price(self):
        return self.product.price * self.quantity
    

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_or_update_cart(sender, instance, created, **kwargs):
#     if created:
#         Cart.objects.create(user=instance)
#     instance.cart.save()


class Order(BaseModel):
    pass
class OrderItems(BaseModel):
    pass