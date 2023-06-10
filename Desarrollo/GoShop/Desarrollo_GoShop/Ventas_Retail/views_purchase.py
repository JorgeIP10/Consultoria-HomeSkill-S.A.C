from .shop_cart import ShopCart
from .models import Product, PaymentCard
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from cryptography.fernet import Fernet
import json

def buy_product(request):
    cards = PaymentCard.objects.filter(owner_id=request.user.id)
    dates = {'months': ['--', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
            'years': ['----', 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034]}
    cart = ShopCart(request)
    products = []
    total_price = 0
    for item in cart.shopcart:
        if (item[0]['sale_price']):
            total_price += (item[0]['sale_price'] * item[0]['quantity'])
        else:
            total_price += (item[0]['price'] * item[0]['quantity'])
        products.append(item[0])

    total_quantity = cart.quantity_products()
    if request.method == 'GET':
        try:
            remembered_card = PaymentCard.objects.get(owner_id=request.user.id, remembered=True)
        except:
            remembered_card = None
        return render(request, 'buy.html', {'products': products, 'total_quantity': total_quantity, 'total_price': total_price, 'cards': cards, 'dates': dates, 'remembered_card': remembered_card.number})
    else:
        if 'confirm-purchase' in request.POST:
            return render(request, 'buy.html', {'products': products, 'total_quantity': total_quantity, 'total_price': total_price, 'cards': cards, 'dates': dates})

def verify_card(request, number, month, year, cvv, remember):
    if (remember == 'false'):
        remember = False
    else:
        remember = True
    
    try:
        remembered_card = PaymentCard.objects.get(owner_id=request.user.id, remembered=True)
    except:
        remembered_card = None
    print(remember)
    if remember:
        try:
            card = PaymentCard.objects.get(owner_id=request.user.id, number=number)
            if (card and not card.remembered):
                card.remembered = True
                card.save()
                if (remembered_card):
                    remembered_card.remembered = False
                    remembered_card.save()
        except:
            PaymentCard.objects.create(owner_id=request.user.id, number=number,
            expiration_month=month, expiration_year=year, cvv=cvv, remembered=True)
            if remembered_card:
                remembered_card.remembered = False
                remembered_card.save()
    return JsonResponse({})