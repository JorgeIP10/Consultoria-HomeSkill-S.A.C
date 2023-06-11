from .shop_cart import ShopCart
from .models import Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse

@login_required
def shopping_cart(request):
    cart = ShopCart(request)
    products_model = Product.objects.all()
    products = []
    id_products = []
    for item in cart.shopcart:
        for product in products_model:
            if product.name == item[0]['name']:
                id_products.append(product.id)
        products.append(item[0])
    
    total_quantity = cart.quantity_products()
    if request.method == 'GET':
        return render(request, 'shopping_cart.html', {'products': products, 'products_model': products_model, 'id_products': id_products, 'total_quantity': total_quantity})
    else:
        return redirect('buy')

def get_product_quantity_cart(request, product_id):
    cart = ShopCart(request)
    quantity = 0
    for article in cart.shopcart:
        if (article[0]['id'] == product_id):
            quantity = article[0]['quantity']
            break
    return JsonResponse({'quantity': quantity})

def add_product(request, product_id):
    cart = ShopCart(request)
    product = list(Product.objects.filter(id=product_id).values('id','name', 'price', 'sale_price', 'image'))
    
    cart.add_product(product)
    for article in cart.shopcart:
        if (product[0]['name'] == article[0]['name']):
            selected_product = article
            break

    total_quantity = cart.quantity_products()
    
    data = {'product': selected_product, 'total_quantity': total_quantity}
    return JsonResponse(data)

def remove_product_unit(request, product_id):
    cart = ShopCart(request)
    cart.remove_product_unit(product_id)
    
    for article in cart.shopcart:
        if (product_id == article[0]['id']):
            selected_product = article
            break
    
    total_quantity = cart.quantity_products()

    data = {'product': selected_product, 'total_quantity': total_quantity}
    return JsonResponse(data)

def remove_product(request, product_id):
    cart = ShopCart(request)
    cart.remove_product(product_id)

    total_price = 0
    for article in cart.shopcart:
        if article[0]['sale_price']:
            total_price += float(article[0]['sale_price']) * float(article[0]['quantity'])
        else:
            total_price += float(article[0]['price']) * float(article[0]['quantity'])
        
    total_quantity = cart.quantity_products()
    data = {'total_quantity': total_quantity, 'total_price': total_price}
    return JsonResponse(data)