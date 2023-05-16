from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
import GoShop.settings as settings
from .models import Product
from.shop_cart import ShopCart
from django.http import JsonResponse

def shop(request):
    if request.method == 'GET':
        # shopcart = ShopCart(request)
        products_kitchen = Product.objects.filter(category_id='Kitchen')[:4]
        products_bathroom = Product.objects.filter(category_id='Bathroom')[:4]
        products_bedroom = Product.objects.filter(category_id='Bedroom')[:4]
        products_decor = Product.objects.filter(category_id='Decor')[:4]
        products_offer = Product.objects.filter(on_sale=True)[:4]
        
        products = {'kitchen': products_kitchen, 'bathroom': products_bathroom, 'bedroom': products_bedroom, 'decor': products_decor, 'offer': products_offer}

        return render(request, 'shop.html', {'products': products})
    else:
        if 'button-search' in request.POST:
            try:
                view_names = {'Kitchen':'kitchen', 'Bathroom':'bathroom', 'Bedroom':'bedroom', 'Decor':'decor'}
                product = Product.objects.get(name=request.POST['search'])
                return redirect('description', view_name=view_names[product.category_id], product_id=product.id)
            except:
                return redirect('description',  view_name='kitchen', product_id=0)

def products(request, category_name, name, view_name):
    if request.method == 'GET':
        products = Product.objects.filter(category=category_name)
        return render(request, 'products.html', {'name': name, 'products': products, 'view': view_name})
    else:
        if 'button-search' in request.POST:
            try:
                product = Product.objects.get(name=request.POST['search'])
                return redirect('description', view_name=view_name, product_id=product.id)
            except:
                return redirect('description',  view_name=view_name, product_id=0)
        elif 'see-description' in request.POST:
            try:
                product = Product.objects.get(id=request.POST['product_id'])
                return redirect('description', view_name=view_name, product_id=product.id)
            except:
                return redirect('description',  view_name=view_name, product_id=0)

def product_description(request, view_name, product_id):
    names = {'kitchen':'Cocina', 'Kitchen':'Cocina', 'bathroom':'Baño', 'Bathroom':'Baño', 'bedroom':'Dormitorio', 'Bedroom':'Dormitorio', 'decor':'Decoración', 'Decor':'Decoración', 'offers':'Ofertas'}
    if request.method == 'GET':
        try:
            product = Product.objects.get(id=product_id)
            return render(request, 'product_description.html', {'product': product, 'previous_view': names[product.category_id],'view': view_name})
        except:
            return render(request, 'product_description.html', {'error': 'No se ha encontrado el producto.', 'previous_view': names[view_name], 'view': view_name})
    else:
        if request.user.is_anonymous:
            return redirect('signin')
        else:
            if 'button-search' in request.POST:
                try:
                    product = Product.objects.get(name=request.POST['search'])
                    return render(request, 'product_description.html', {'product': product, 'previous_view': names[product.category_id],'view': view_name})
                except:
                    return render(request, 'product_description.html', {'error': 'No se ha encontrado el producto.', 'previous_view': names[view_name], 'view': view_name})
            elif 'see-description' in request.POST:
                try:
                    product = Product.objects.get(id=request.POST['product_id'])
                    return redirect('description', view_name=view_name, product_id=product.id)
                except:
                    return redirect('description',  view_name=view_name, product_id=0)
            elif 'shopcart-button' in request.POST:
                return redirect('cart')

def kitchen(request):
    return products(request, 'Kitchen', 'Cocina', 'kitchen')

def bathroom(request):
    return products(request, 'Bathroom', 'Baño', 'bathroom')

def bedroom(request):
    return products(request, 'Bedroom', 'Dormitorio', 'bedroom')

def decor(request):
    return products(request, 'Decor', 'Decoración', 'decor')

def offers(request):
    if request.method == 'GET':
        products = Product.objects.filter(on_sale=True)
        return render(request, 'products.html', {'name': 'Ofertas', 'products': products, 'view': 'offers'})
    else:
        names = {'Kitchen':'kitchen', 'Bathroom':'bathroom', 'Bedroom':'bedroom','Decor':'decor'}
        if 'button-search' in request.POST:
            try:
                product = Product.objects.get(name=request.POST['search'])
                return redirect('description', view_name=names[product.category_id], product_id=product.id)
            except:
                return redirect('description', view_name='offers', product_id=0)
            
        elif 'see-description' in request.POST:
            try:
                product = Product.objects.get(id=request.POST['product_id'])
                return redirect('description', view_name=names[product.category_id], product_id=product.id)
            except:
                return redirect('description',  view_name='offers', product_id=0)


def get_products(request, text):
    products = list(Product.objects.values())
    names_products = []
    for product in products:
        if product['name'].lower().startswith(text.lower()):
            names_products.append(product['name'])

    data = {'products': names_products}
    return JsonResponse(data)