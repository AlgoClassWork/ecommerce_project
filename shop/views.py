from django.shortcuts import render, get_object_or_404

from .models import *

def product_list(request, slug=None):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()

    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=category)

    context = {'products':products, 'categories':categories}
    return render(request, 'product_list.html', context)