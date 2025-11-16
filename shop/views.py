from django.shortcuts import render, redirect, get_object_or_404

from .models import *
from .forms import *

def product_list(request, slug=None):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()

    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=category)

    context = {'products':products, 'categories':categories}
    return render(request, 'product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    reviews = product.reviews.all()
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.product = product
            new_review.save()
            return redirect('product_detail', product.slug)

    context = {'product':product, 'reviews':reviews, 'form':form}
    return render(request, 'product_detail.html', context)


def cart_detail(request):
    cart = request.session.get('cart', {})
    product_slugs = cart.keys() 
    products = Product.objects.filter(slug__in=product_slugs)
    
    total_price = 0
    cart_products = []
    for product in products:
        quantity = cart[product.slug]
        total_item = product.price * quantity
        cart_products.append( {'product':product, 'quantity': quantity, 'total_price': total_item} )
        total_price += total_item

    context = {'cart_products':cart_products, 'total_price':total_price}
    return render(request, 'cart_detail.html', context)

def cart_add(request, slug):
    cart = request.session.get('cart', {})
    quantity = cart.get( slug, 0 ) + 1
    cart[slug] = quantity
    request.session['cart'] = cart
    return redirect( 'product_list' )

def cart_clear(request):
    request.session['cart'] = {}
    return redirect( 'cart_detail' )

def cart_remove(request, slug):
    cart = request.session.get('cart', {})
    if slug in cart:
        del cart[slug]
        request.session['cart'] = cart
    return redirect('cart_detail')

def order_create(request):
    if request.method == 'GET':
        form = OrderCreateForm()
        context = {'form':form}
        return render(request, 'order_create.html', context)
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        form = OrderCreateForm(request.POST)
        order = form.save(commit=False)
        product_slugs = cart.keys()
        products = Product.objects.filter(slug__in=product_slugs)
        items_text = []
        total_cost = 0
        for product in products:
            quantity = cart[product.slug]
            total_price = quantity * product.price
            items_text.append(f'{product.name} - {quantity} шт - {total_price} сом')
            total_cost += total_price

        order.products = '\n'.join(items_text)
        order.total_cost = total_cost
        order.save()

        request.session['cart'] = {}
        context = {'order': order}
        return render(request, 'order_created.html', context)


