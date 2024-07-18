from django.urls import path
from . import views


urlpatterns = [
    
    path('<slug>/' , views.get_product , name="get_product"),
    # path('', views.product_list, name='product_list'),
    # path('<int:product_id>/', views.product_detail, name='product_detail'),
    # path('category/<int:category_id>/', views.category_products, name='category_products'),
   
]