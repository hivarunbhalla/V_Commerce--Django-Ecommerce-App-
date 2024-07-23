from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Product, SizeVariant, Category

def get_product(request, slug):
    product = get_object_or_404(Product, slug=slug)
    size_variants = product.size_variants.all()

    # Get the selected variant prices
    selected_size = request.GET.get('size')
    
    variant_price = product.product_price
    if selected_size:
        size_variant = size_variants.filter(size_name=selected_size).first()
        if size_variant:
            variant_price = size_variant.varient_price

    context = {
        'product': product,
        'size_variants': size_variants,
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