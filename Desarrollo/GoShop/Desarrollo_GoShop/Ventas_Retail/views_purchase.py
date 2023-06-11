from .shop_cart import ShopCart
from .models import Product, PaymentCard, UserInfo
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse

def buy_product(request):
    cards = PaymentCard.objects.filter(owner_id=request.user.id)
    dates = {'months': ['--', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
            'years': ['----', 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034]}
    cart = ShopCart(request)
    products = []
    total_price = 0
    for item in cart.shopcart[-1]['products']:
        if (item['sale_price']):
            total_price += (item['sale_price'] * item['quantity'])
        else:
            total_price += (item['price'] * item['quantity'])
        products.append(item)

    total_quantity = cart.quantity_products()
    if request.method == 'GET':
        try:
            remembered_card = PaymentCard.objects.get(owner_id=request.user.id, remembered=True)
            if (UserInfo.objects.filter(user_id=request.user.id)):
                user = UserInfo.objects.get(user_id=request.user.id)
                return render(request, 'buy.html', {'products': products, 'total_quantity': total_quantity, 'total_price': total_price, 'cards': cards, 'dates': dates, 'remembered_card': remembered_card.number, 'names': user.names, 'surnames': user.surnames})
            return render(request, 'buy.html', {'products': products, 'total_quantity': total_quantity, 'total_price': total_price, 'cards': cards, 'dates': dates, 'remembered_card': remembered_card.number})
        except:
            if (UserInfo.objects.filter(user_id=request.user.id)):
                user = UserInfo.objects.get(user_id=request.user.id)
                return render(request, 'buy.html', {'products': products, 'total_quantity': total_quantity,'total_price': total_price, 'cards': cards, 'dates': dates, 'names': user.names, 'surnames': user.surnames})
            return render(request, 'buy.html', {'products': products, 'total_quantity': total_quantity, 'total_price': total_price, 'cards': cards, 'dates': dates})
    else:
        if 'confirm-purchase' in request.POST:
            checkbox = request.POST.get('remember-card', False)
            remember = False
            if (checkbox):
                remember = True
            
            try:
                remembered_card = PaymentCard.objects.get(owner_id=request.user.id, remembered=True)
            except:
                remembered_card = None
            if remember:
                try:
                    card = PaymentCard.objects.get(owner_id=request.user.id, number=request.POST['card'])
                    if (card and not card.remembered):
                        card.remembered = True
                        card.save()
                        if (remembered_card):
                            remembered_card.remembered = False
                            remembered_card.save()
                except:
                    PaymentCard.objects.create(owner_id=request.user.id, number=request.POST['card'],
                    expiration_month=request.POST['select-month'], expiration_year=request.POST['select-year'], cvv=request.POST['cvv'], remembered=True)
                    if remembered_card:
                        remembered_card.remembered = False
                        remembered_card.save()
            
            cart = ShopCart(request)
            products = Product.objects.all()
            quantity = cart.quantity_products()
            i = 0
            for item in cart.shopcart[-1]['products']:
                for product in products:
                    if product.id == item['id']:
                        product.stock -= item['quantity']
                        product.save()
                        i += 1
                    if i == quantity:
                        break
            
            cart.set_purchased()
            redirect_url = reverse('confirm_purchase', kwargs={'previous_view': 'buy', 'previous_name': 'Realizar compra', 'mode': 'confirm_purchase'})
            return redirect(redirect_url)
        
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
    return render(request, 'confirm_data.html', {'previous_view': previous_view, 'previous_name': previous_name, 'mode': mode})