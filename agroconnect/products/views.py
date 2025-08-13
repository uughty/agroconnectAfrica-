# products/views.py
# This file is updated to include a new 'home' view.

from django.shortcuts import render
from .models import Product

def home(request):
    """
    View for the homepage, displaying a few featured products.
    """
    featured_products = Product.objects.order_by('?')[:3] # Get 3 random products
    context = {'featured_products': featured_products}
    return render(request, 'index.html', context)

def product_list(request):
    """
    View to display a list of all products from the database.
    """
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'products/product_list.html', context)