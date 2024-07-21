from typing import Any
from django.shortcuts import render
from django.views.generic import TemplateView

class Cart(TemplateView):
    template_name = 'orders/cart.html'

    #select relat or prefetch related for varient of product

    # def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
    #     context = {
    #         'cart_items' : self.
    #     }
    #     return context
    