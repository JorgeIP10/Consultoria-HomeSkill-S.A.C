from .shop_cart import ShopCart
from .models import Product, PaymentCard, UserInfo
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .forms import CustomPayPalPaymentsForm, FormWithCaptcha
from django.conf import settings
import uuid
import json

def buy_product(request):
    if request.method == 'GET':
        cart = ShopCart(request)
        products = []
        total_price = 0

        for item in cart.shopcart[-1]['products']:
            if (item['sale_price']):
                total_price += (item['sale_price'] * item['quantity'])
            else:
                total_price += (item['price'] * item['quantity'])
        total_price = round(total_price, 2)
        total_quantity = cart.quantity_products()

        for item in cart.shopcart[-1]['products']:
            if item['sale_price']:
                products.append({'name': item['name'], 'price': item['sale_price'], 'quantity': item['quantity']})
            else:
                products.append({'name': item['name'], 'price': item['price'], 'quantity': item['quantity']})
        
        paypal_dict = '{'
        paypal_dict += f'"business": "{settings.PAYPAL_RECEIVER_EMAIL}", "cmd": "_cart", "upload": "1", '

        purchase_ok = {'previous_view': 'buy', 'previous_name': 'Realizar compra', 'mode': 'purchase-ok'}
        purchase_error = {'previous_view': 'buy', 'previous_name': 'Realizar compra', 'mode': 'purchase-error'}
        paypal_dict += f'"num_cart_items": {cart.quantity_products()}, '
        cont = 1

        for product in products:
            paypal_dict += f'"item_name_{cont}": "{product["name"]}", "amount_{cont}": {product["price"]}, "quantity_{cont}": {product["quantity"]}, '
            cont += 1
        
        paypal_dict += f'"shipping_1": {10*cart.quantity_products()}, '
        paypal_dict += f'"invoice": "{str(uuid.uuid4())}", "notify_url": "{request.build_absolute_uri(reverse("paypal-ipn"))}", "return": "{request.build_absolute_uri(reverse("confirm_purchase", kwargs=purchase_ok))}", "cancel_return": "{request.build_absolute_uri(reverse("confirm_purchase", kwargs=purchase_error))}"'
        paypal_dict += "}"
        paypal_dict = json.loads(paypal_dict)
        paypal_form = CustomPayPalPaymentsForm(initial=paypal_dict)
        captcha_form = FormWithCaptcha()

        if (UserInfo.objects.filter(user_id=request.user.id)):
            user = UserInfo.objects.get(user_id=request.user.id)
            return render(request, 'buy.html', {'total_quantity': total_quantity, 'total_price': total_price, 'names': user.names, 'surnames': user.surnames, 'captcha_form': captcha_form, 'paypal_form': paypal_form})
        
        return render(request, 'buy.html', {'total_quantity': total_quantity, 'total_price': total_price, 'captcha_form': captcha_form, 'paypal_form': paypal_form})
        
def save_user_info(request, names, surnames, dni, address):
    try:
        user_info = UserInfo.objects.get(user_id=request.user.id)
        if names != user_info.names: user_info.names = names
        if surnames != user_info.surnames: user_info.surnames = surnames
        if dni != user_info.dni: user_info.dni = dni
        if address != user_info.address: user_info.address = address
        user_info.save()
        return HttpResponse(status=200)
    except:
        UserInfo.objects.create(user_id = request.user.id, names = names, surnames = surnames, dni = dni, address = address)
        return HttpResponse(status=200)

def confirm_purchase(request, previous_view, previous_name, mode):
    if (mode == 'purchase-ok'):
        cart = ShopCart(request)
        products = Product.objects.all()
        for item in cart.shopcart[-1]['products']:
            for product in products:
                if product.id == item['id']:
                    product.stock -= item['quantity']
                    product.save()
        cart.set_purchased()
    return render(request, 'confirm_data.html', {'previous_view': previous_view, 'previous_name': previous_name, 'mode': mode})