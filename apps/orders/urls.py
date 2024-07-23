# from django.urls import path
# from . import views

# urlpatterns = [
#     # path('', views.order_list, name='order_list'),
#     # path('<int:order_id>/', views.order_detail, name='order_detail'),
#     # path('create/', views.create_order, name='create_order'),
#     path('cart/', views.cart_view , name = 'cart')
    
# ]

from django.urls import path
from .views import(add_to_cart,
                remove_from_cart,
                update_cart,
                cart_view,
                create_order,
                order_view,
                order_list)

urlpatterns = [
    path('cart/add/<uuid:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<uuid:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<uuid:cart_item_id>/', update_cart, name='update_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('order/create/', create_order, name='create_order'),
    path('order/<uuid:order_id>/', order_view, name='order_view'),
    path('orders/', order_list, name='order_list'),
]
