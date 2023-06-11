from django.urls import reverse
from django.shortcuts import render
from .forms import CustomPayPalPaymentsForm
from django.conf import settings
import uuid
from .shop_cart import ShopCart
import json

def paypal(request):
    # cart = ShopCart(request)
    # products = []
    # for item in cart.shopcart[-1]['products']:
    #     if item['sale_price']:
    #         products.append({'name': item['name'], 'price': item['sale_price'], 'quantity': item['quantity']})
    #     else:
    #         products.append({'name': item['name'], 'price': item['price'], 'quantity': item['quantity']})
    
    # paypal_dict = '{'
    # paypal_dict += f'"business": "{settings.PAYPAL_RECEIVER_EMAIL}", "cmd": "_cart", "upload": "1", '

    # purchase_ok = {'previous_view': 'buy', 'previous_name': 'Realizar compra', 'mode': 'purchase-ok'}
    # purchase_error = {'previous_view': 'buy', 'previous_name': 'Realizar compra', 'mode': 'purchase-error'}
    # paypal_dict += f'"num_cart_items": {cart.quantity_products()}, '
    # cont = 1
    # for product in products:
    #     paypal_dict += f'"item_name_{cont}": "{product["name"]}", "amount_{cont}": {product["price"]}, "quantity_{cont}": {product["quantity"]}, '
    #     cont += 1
    # paypal_dict += f'"shipping_1": {10*cart.quantity_products()}, '
    # paypal_dict += f'"invoice": "{str(uuid.uuid4())}", "notify_url": "{request.build_absolute_uri(reverse("paypal-ipn"))}", "return": "{request.build_absolute_uri(reverse("confirm_purchase", kwargs=purchase_ok))}", "cancel_return": "{request.build_absolute_uri(reverse("confirm_purchase", kwargs=purchase_error))}"'
    # paypal_dict += "}"

    # print(paypal_dict)
    # for product in products:
    #     if product.id == item['id']:
    #         product.stock -= item['quantity']
    #         product.save()
    #         i += 1
    #     if i == quantity:
    #         break
    a = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        # "cmd": "_cart",
        # "upload": "1",
        # "handling_cart": "1",
        # "shipping2": 0,
        # "tax_cart": "15",
        # "shopping_url": "http://127.0.0.1:8000/",
        # "num_cart_items": 3,
        # "item_name_1": "Item 1",
        # "amount_1": 10.00,
        # "quantity_1": 2,
        # "shipping_1": 10*2,
        # "item_name_2": "Item 2",
        # "amount_2": 15.00,
        # "quantity_2": 1,
        # "shipping_2": 10*1,
        # "item_name_3": "Item 3",
        # "amount_3": 5.00,
        # "quantity_3": 3,
        # "shipping_3": 10*3,
        # 'num_cart_items': 1,
        # "item_name_1": "ana",
        # "amount_1": 1.00,
        # "quantity_1": 1,
        'item_name': 'a',
        'quantity': 1,
        'amount': 1.0,
        "invoice": str(uuid.uuid4()),
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('successful_payment')),
        "cancel_return": request.build_absolute_uri(reverse('payment_error')),
        # "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }
    # print(a)
    # paypal_dict = json.loads(paypal_dict)
    # print(paypal_dict)
    # print(type(paypal_dict))
    # paypal_dict = '{ "business": "example@example.com", "cmd": "_cart", "upload": "1", "num_cart_items": 3, "item_name_1": "Item 1", "amount_1": 10.00, "quantity_1": 2, "item_name_2": "Item 2", "amount_2": 15.00, "quantity_2": 1, "item_name_3": "Item 3", "amount_3": 5.00, "quantity_3": 3, "shipping_1": 30.00, "invoice": "123456", "notify_url": "http://example.com/paypal-ipn", "return": "http://example.com/successful_payment", "cancel_return": "http://example.com/payment_error" }'

    # paypal_dict = json.loads(paypal_dict)
    # print(paypal_dict)

    # Create the instance.
    form = CustomPayPalPaymentsForm(initial=a)
    context = {"form": form}
    return render(request, "paypal.html", context)

def payment_error(request):
    return render(request, 'payment_error.html')

def successful_payment(request):
    return render(request, 'successful_payment.html')