from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Product, Category

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import Product

def get_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    variants = product.variants.all()

    # Determine the initially selected variant
    selected_variant_uid = request.GET.get('variant_uid')
    initial_variant = variants.first()

    variant_price = product.product_price
    if selected_variant_uid:
        variant = variants.filter(uid=selected_variant_uid).first()
        if variant:
            variant_price = variant.varient_price
    elif initial_variant:
        variant_price = initial_variant.varient_price

    context = {
        'product': product,
        'variants': variants,
        'variant_price': variant_price,
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'price': float(variant_price)})
    
    return render(request, 'product/product.html', context)

def product_list(request):
    products = Product.objects.all()
    context = {
        'products' : products
    }
    return render(request, 'product/all_list.html', context)

def category_list(request):
    categories = Category.objects.all()
    context = {
        'categories' : categories
    }
    return render(request, 'product/all_list.html', context)