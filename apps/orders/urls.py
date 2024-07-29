# from django.urls import path
# from . import views

# urlpatterns = [
#     # path('', views.order_list, name='order_list'),
#     # path('<int:order_id>/', views.order_detail, name='order_detail'),
#     # path('create/', views.create_order, name='create_order'),
#     path('cart/', views.cart_view , name = 'cart')
    
# ]

from django.urls import path
from .views import(
    add_to_cart,
    cart_view,
    remove_from_cart,
    update_cart,
    remove_coupon,

    # create_order,
    # order_list,
    # order_detail,
    # update_order,
    # delete_order,
    OrderDetailView,
    )

urlpatterns = [
    # path('cart/add/<uuid:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/add/<uuid:product_uid>/<uuid:variant_uid>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart_view'),
    path('cart/remove/<uuid:cart_item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<uuid:cart_item_id>/', update_cart, name='update_cart'),

    path('remove_coupon/<uuid:cart_id>/', remove_coupon, name='remove_coupon'),

    # path('create/', create_order, name='create_order'),
    # path('order_list/', order_list, name='order_list'),
    path('<uuid:order_id>/', OrderDetailView.as_view(), name='order_detail'),
    # path('<uuid:order_id>/update/', update_order, name='update_order'),
    # path('<uuid:order_id>/delete/', delete_order, name='delete_order'),
]
#     path('create/', create_order, name='create_order'),
#     path('order_list/', order_list, name='order_list'),
#     path('<uuid:order_id>/', order_detail, name='order_view'),
#     path('<uuid:order_id>/update/', update_order, name='update_order'),
#     path('<uuid:order_id>/delete/', delete_order, name='delete_order'),
# ]
