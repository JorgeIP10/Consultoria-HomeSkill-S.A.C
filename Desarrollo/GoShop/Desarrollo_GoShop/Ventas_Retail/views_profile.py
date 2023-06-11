from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import PaymentCard
from .utils import render_to_pdf
from .shop_cart import ShopCart
import base64

@login_required                
def user_profile(request):
    return render(request, 'user_profile.html')

@login_required                
def user_config(request):
    if request.method == 'GET':
        return render(request, 'user_config.html')
    else:
        if 'confirm-username' in request.POST:
            if (User.objects.get(id=request.user.id).check_password(request.POST['password'])):
                user = User.objects.get(id=request.user.id)
                user.username = request.POST['username']
                user.save()
                return redirect('confirm_user_config', previous_view='config', previous_name='Tus datos', mode='username')
            else:
                return render(request, 'user_config.html', {'error_username': 'La contraseña es incorrecta.'})
        else:
            user = User.objects.get(id=request.user.id)
            if (user.check_password(request.POST['current-password'])):
                user.set_password(request.POST['new-password'])
                user.save()
                user_auth = authenticate(username=request.user.username, password=request.POST['new-password'])
                login(request, user_auth)
                return redirect('confirm_user_config', previous_view='config', previous_name='Tus datos', mode='password')
            else:
                return render(request, 'user_config.html', {'error_password': 'La contraseña actual es incorrecta.'})
            
def confirm_user_config(request, previous_view, previous_name, mode):
    return render(request, 'confirm_data.html', {'previous_view': previous_view, 'previous_name': previous_name, 'mode': mode})

@login_required                
def user_payment(request):
    cards = PaymentCard.objects.filter(owner_id=request.user.id)
    dates = {'months': ['--', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
            'years': ['----', 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034]}
    if request.method == 'GET':
        return render(request, 'user_payment.html', {'cards': cards, 'dates': dates})
    else:
        if 'button-remember-card' in request.POST:
            try:
                card_remembered = PaymentCard.objects.get(owner_id=request.user.id, remembered=True)
                if (card_remembered.id != request.POST['remember-card'] and
                    card_remembered.owner_id == request.user.id):
                    card_remembered.remembered = False
                    card_remembered.save()

                    new_card_remembered = PaymentCard.objects.get(id=request.POST['remember-card'])
                    new_card_remembered.remembered = True
                    new_card_remembered.save()
            except:
                PaymentCard.objects.filter(owner_id=request.user.id, id=request.POST['remember-card']).update(remembered=True)
            
            return redirect('confirm_payment', previous_view='payment', previous_name='Métodos de pago', mode='remember-card')
        else:
            try:
                PaymentCard.objects.get(owner_id=request.user.id, number=request.POST['card'])
                cards = PaymentCard.objects.filter(owner_id=request.user.id)
                dates = {'months': ['--', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
                    'years': ['----', 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034]}
                
                return render(request, 'user_payment.html', {'cards': cards, 'dates': dates,'error': 'No se puede agregar la misma tarjeta.'})
            except:
                PaymentCard.objects.create(owner_id=request.user.id, number=request.POST['card'],
                expiration_month=request.POST['select-month'],
                expiration_year=request.POST['select-year'],
                cvv=request.POST['cvv'])

                return redirect('confirm_payment', previous_view='payment', previous_name='Métodos de pago', mode='add-card')
        
def confirm_payment(request, previous_view, previous_name, mode):
    return render(request, 'confirm_data.html', {'previous_view': previous_view, 'previous_name': previous_name, 'mode': mode})

def shopping_history(request):
    cart = ShopCart(request)
    list_products = []
    total_amount = 0
    for item in cart.shopcart:
        cont = 0
        cont_products_quantity = 0
        cont_rows = 0
        cart_amount = 0
        for article in item['products']:
            if item['status'] and cont != 1:
                article['purchased'] = item['status']['purchased']
                article['purchase_time'] = item['status']['purchase_time']
                cont += 1
            elif cont == 0:
                break
            
            if article['sale_price']:
                article['total_price'] = float(article['sale_price']) * float(article['quantity'])
                cart_amount += article['total_price']
            else:
                article['total_price'] = float(article['price']) * float(article['quantity'])
                cart_amount += article['total_price']

            if cont_products_quantity != 1:
                article['rows_quantity'] = len(item['products'])
                cont_products_quantity += 1
            
            cont_rows += 1
            if cont_rows == len(item['products']):
                article['new_row'] = True
                article['cart_amount'] = cart_amount
                total_amount += cart_amount

            list_products.append(article)

    products = {'products': list_products, 'total_amount': round(total_amount, 2)}

    pdf = render_to_pdf('shopping_history_pdf.html', products)
    pdf_data_base64 = base64.b64encode(pdf).decode('utf-8')
    return render(request, 'shopping_history.html', {'pdf': pdf_data_base64})