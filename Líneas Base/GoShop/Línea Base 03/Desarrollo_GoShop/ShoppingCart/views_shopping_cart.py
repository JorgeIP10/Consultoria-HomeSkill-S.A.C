from .shop_cart import ShopCart
from Ventas_Retail.models import Product
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse

@login_required
def shopping_cart(request):
    cart = ShopCart(request)
    products_model = Product.objects.all()
    products = []
    id_products = []

    total_quantity = 0
    if (not cart.shopcart[-1]['products']):
        products = []
    else:
        for item in cart.shopcart[-1]['products']:
            for product in products_model:
                if product.name == item['name']:
                    id_products.append(product.id)
            products.append(item)
    
        total_quantity = cart.quantity_products()
    
    if request.method == 'GET':
        return render(request, 'shopping_cart.html', {'products': products, 'products_model': products_model, 'id_products': id_products, 'total_quantity': total_quantity})
    else:
        if 'button-search' in request.POST:
            names = {'Kitchen':'kitchen', 'Bathroom':'bathroom', 'Bedroom':'bedroom','Decor':'decor'}
            try:
                product = Product.objects.get(name=request.POST['search'])
                return redirect('description', view_name=names[product.category_id], product_id=product.id)
            except:
                return redirect('description', view_name='kitchen', product_id=0)
        else:
            return redirect('buy')

def get_product_quantity_cart(request, product_id):
    cart = ShopCart(request)
    quantity = 0
    if cart.shopcart[-1]['products']:
        for article in cart.shopcart[-1]['products']:
            if (article['id'] == product_id):
                quantity = article['quantity']
                break
    return JsonResponse({'quantity': quantity})

def add_product(request, product_id):
    cart = ShopCart(request)
    product = list(Product.objects.filter(id=product_id).values('id','name', 'price', 'sale_price', 'image'))
    
    cart.add_product(product[0])
    for article in cart.shopcart[-1]['products']:
        if (product[0]['name'] == article['name']):
            selected_product = article
            break

    total_quantity = cart.quantity_products()
    data = {'product': selected_product, 'total_quantity': total_quantity}
    return JsonResponse(data)

def remove_product_unit(request, product_id):
    cart = ShopCart(request)
    cart.remove_product_unit(product_id)
    
    selected_product = None
    for article in cart.shopcart[-1]['products']:
        if (product_id == article['id']):
            selected_product = article
            break
    
    total_quantity = cart.quantity_products()
    data = {'product': selected_product, 'total_quantity': total_quantity}
    return JsonResponse(data)

def remove_product(request, product_id):
    cart = ShopCart(request)
    cart.remove_product(product_id)
    if (cart.shopcart[-1]['products']):
        total_price = 0
        for article in cart.shopcart[-1]['products']:
            if article['sale_price']:
                total_price += float(article['sale_price']) * float(article['quantity'])
            else:
                total_price += float(article['price']) * float(article['quantity'])
        total_quantity = cart.quantity_products()
        data = {'total_quantity': total_quantity, 'total_price': total_price}
        return JsonResponse(data)
    else:
        return JsonResponse({})