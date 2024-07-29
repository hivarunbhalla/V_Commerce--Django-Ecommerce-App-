from django.shortcuts import render
from ..products.models import Product

def home_page(request):
    context = {
        'products': Product.objects.all(),
        # 'first_varient_price': display_price
    }
    return render(request, 'pages\home.html', context=context)
