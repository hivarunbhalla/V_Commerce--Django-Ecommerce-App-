# from django.shortcuts import render
# from .models import Cart, CartItem
# # from django.shortcuts import get_or_create

# def cart_view(request):
#     pass
    


# def add_to_cart(request, product_id):
#     pass

#     # https://www.perplexity.ai/search/write-a-view-for-cart-in-djang-_l__dOySSNy6.wqED6adsw

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic.detail import DetailView
from .models import Cart, CartItem, Order, OrderItem, Product, ProductVariant

from apps.promotions.models import Coupon

'''
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, uid=product_id)
    
    # Create or get the cart from the session for anonymous users
    cart_id = request.session.get('cart_id')
    
    if cart_id:
        cart = get_object_or_404(Cart, uid=cart_id)
    else:
        cart = Cart.objects.create()  # Create a new cart for anonymous user
        request.session['cart_id'] = str(cart.uid)  # Convert UUID to string
    
    # Check if the product is already in the cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    # Redirect to cart view after adding the item to cart
    return redirect('cart_view')
'''

def add_to_cart(request, product_uid, variant_uid):
    product = get_object_or_404(Product, uid=product_uid)
    variant = get_object_or_404(ProductVariant, uid=variant_uid)

    # Create or get the cart from the session for anonymous users
    cart_id = request.session.get('cart_id')
    
    if cart_id:
        cart = get_object_or_404(Cart, uid=cart_id)
    else:
        cart = Cart.objects.create()  # Create a new cart for anonymous user
        request.session['cart_id'] = str(cart.uid)  # Convert UUID to string
    
    # Check if the product variant is already in the cart
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        variant=variant,
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    # Redirect to cart view after adding the item to cart
    return redirect('cart_view')


def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, uid=cart_item_id)
    cart_item.delete()
    return redirect('cart_view')

def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, uid=cart_item_id)
    quantity = int(request.POST.get('quantity', 1))
    cart_item.quantity = quantity
    cart_item.save()
    return redirect('cart_view')

# def cart_view(request):
#     cart_id = request.session.get('cart_id')
#     cart_obj = get_object_or_404(Cart, uid=cart_id) if cart_id else None
#     cart_items = cart_obj.cart_items.all() if cart_obj else None
#     # total_price_before_coupon = sum(item.quantity * item.product.product_price for item in cart_items)

#     if request.method == 'POST':
#         code = request.POST.get('coupon-code')
#         try:
#             coupon = Coupon.objects.get(code=code)

#             if cart_obj.coupon == coupon:
#                 messages.warning(request, "This coupon is already applied!")
#             elif not coupon.is_valid():
#                 messages.warning(request, "Invalid Coupon!")
#             else:
#                 cart_obj.coupon = coupon
#                 cart_obj.save()
#                 messages.success(request, "Coupon Applied🎉!")

#         except Coupon.DoesNotExist:
#             messages.warning(request, "Invalid Coupon!")

#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))   
       
    
#     context = {
#         'cart_obj' : cart_obj,
#         'cart_items': cart_items,
#         }
#     context.update(get_prices(request, cart_obj))
    
#     return render(request, 'orders/cart.html', context=context)


def apply_coupon(request, cart_obj):
    code = request.POST.get('coupon-code')
    try:
        coupon = Coupon.objects.get(code=code)
        if cart_obj.coupon == coupon:
            messages.warning(request, "This coupon is already applied!")
        elif not coupon.is_valid():
            messages.warning(request, "Invalid Coupon!")
        else:
            cart_obj.coupon = coupon
            cart_obj.save()
            messages.success(request, "Coupon Applied🎉!")
    except Coupon.DoesNotExist:
        messages.warning(request, "Invalid Coupon!")

def cart_view(request):
    cart = get_cart(request)
    cart_items = cart.cart_items.all()
    
    if request.method == 'POST':
        apply_coupon(request, cart)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    context = {
        'cart_obj': cart,
        'cart_items': cart_items,
    }
    context.update(get_prices(request, cart))
    return render(request, 'orders/cart.html', context=context)


def get_prices(request, cart_obj):
    cart_items = cart_obj.cart_items.all() if cart_obj else []
    before_coupon_price = sum(item.quantity * item.variant.varient_price for item in cart_items)
    discount = 0
    final_price = before_coupon_price

    if cart_obj and cart_obj.coupon:
        if cart_obj.coupon.minimum_amount <= before_coupon_price:
            discount = cart_obj.coupon.apply_discount(before_coupon_price)
            final_price = before_coupon_price - discount
        else:
            messages.warning(request, "Minimum purchase amount not reached for coupon.")
            final_price = before_coupon_price

    return {
        'total_price_before_discount': before_coupon_price,
        'discount': discount,
        'total_price_after_discount': final_price
    }

def remove_coupon(request, cart_id):
    try:
        cart = Cart.objects.get(uid = cart_id)
        cart.coupon = None
        cart.save()
        messages.success(request, "Removed coupon successfully!")


    except Cart.DoesNotExist:
        messages.warning(request, "Unable to remove coupon!")

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))  


def get_cart(request):
    cart_id = request.session.get('cart_id')
    return get_object_or_404(Cart, uid=cart_id) if cart_id else Cart.objects.create()

# Order Views

# @login_required
class CreateOrderView(View):
    def post(self, request, *args, **kwargs):
        cart_id = request.session.get('cart_id')
        cart = get_object_or_404(Cart, uid=cart_id)

        if not cart.cart_items.exists():
            messages.warning(request, "Your cart is empty.")
            return redirect('cart_view')

        order = Order.objects.create(
            user=cart.user,
            shipping_address=request.POST.get('shipping_address'),
            billing_address=request.POST.get('billing_address'),
            coupon=cart.coupon,
        )

        for cart_item in cart.cart_items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.product_price
            )

        order.apply_coupon()
        order.total_price = order.discounted_total
        order.save()

        cart.cart_items.all().delete()
        cart.coupon = None
        cart.save()

        messages.success(request, "Order created successfully!")
        return redirect(reverse('order_detail', kwargs={'pk': order.pk}))


# @login_required
class OrderDetailView(DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_object(self):
        order = get_object_or_404(Order, pk=self.kwargs['order_id'], user=self.request.user)
        return order

# @login_required
def order_list(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
        return render(request, 'orders/order_list.html', {'orders': orders})
    else:
        return redirect('login')


def update_order(request):
    # address before shipping
    # payment method
    pass

def cancel_order(request):
    # can cancel before shippipped
    # After that can request 
    pass