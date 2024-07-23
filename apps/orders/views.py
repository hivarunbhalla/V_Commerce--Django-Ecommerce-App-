# from django.shortcuts import render
# from .models import Cart, CartItem
# # from django.shortcuts import get_or_create

# def cart_view(request):
#     pass
    


# def add_to_cart(request, product_id):
#     pass

#     # https://www.perplexity.ai/search/write-a-view-for-cart-in-djang-_l__dOySSNy6.wqED6adsw

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from .models import Cart, CartItem, Order, OrderItem, Product


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

def cart_view(request):
    cart_id = request.session.get('cart_id')
    cart = get_object_or_404(Cart, uid=cart_id) if cart_id else None
    cart_items = cart.cart_items.all() if cart else None
    total_price = sum(item.quantity * item.product.product_price for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_price': total_price
        }
    return render(request, 'orders/cart.html', context=context)

# Order Views

def create_order(request):
    cart_id = request.session.get('cart_id')
    cart = get_object_or_404(Cart, uid=cart_id) if cart_id else None
    cart_items = cart.items.all() if cart else []
    total_price = sum(item.quantity * item.price for item in cart_items)

    if request.method == 'POST':
        if request.user.is_authenticated:
            shipping_address = request.POST.get('shipping_address')
            billing_address = request.POST.get('billing_address')
            order = Order.objects.create(
                user=request.user,
                total_price=total_price,
                shipping_address=shipping_address,
                billing_address=billing_address
            )
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.price
                )
            cart.items.all().delete()  # Clear the cart
            del request.session['cart_id']  # Clear the cart ID from session
            return redirect('order_view', order_id=order.id)
        else:
            # Redirect to login if the user is not authenticated
            return redirect('login')

    return render(request, 'order/create.html', {'cart_items': cart_items, 'total_price': total_price})

def order_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = order.items.all()
    return render(request, 'orders/cart.html', {'order': order, 'order_items': order_items})

def order_list(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
        return render(request, 'order/list.html', {'orders': orders})
    else:
        return redirect('login')

