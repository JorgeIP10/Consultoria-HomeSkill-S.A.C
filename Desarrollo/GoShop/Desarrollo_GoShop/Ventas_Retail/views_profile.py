from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import PaymentCard, ShoppingHistory, ShoppingCart
from django.http import HttpResponse
from django.views.decorators.clickjacking import xframe_options_exempt
from .utils import render_to_pdf
from .shop_cart import ShopCart

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

def show_pdf(request):
    pdf = ShoppingHistory.objects.get(user_id=request.user.id)  # Obtén el PDF desde la base de datos o como mejor aplique a tu caso

    # Define la ruta completa al archivo PDF
    ruta_pdf = pdf.file.path

    # Lee el contenido del archivo PDF
    with open(ruta_pdf, 'rb') as f:
        pdf_data = f.read()

    # Renderiza el PDF en el navegador
    response = HttpResponse(pdf_data, content_type='application/pdf')

    # Establece el encabezado para la descarga del archivo PDF
    response['Content-Disposition'] = 'attachment; filename="nombre_archivo.pdf"'

    return response


def shopping_history(request):
    # url_pdf = '/profile/history/pdf'  # Cambia el ID por el adecuado según tus datos
    # pdf = ShoppingHistory.objects.get(user_id=request.user.id)

    # return render(request, 'shopping_history.html', {'pdf': pdf})
    cart = list(ShoppingCart.objects.filter(user_id=request.user.id).values('items'))
    # print(cart)
    list_products = []
    a = {}
    for item in cart[0]['items']:
        if item[0]['sale_price']:
            item[0]['total_price'] = float(item[0]['sale_price']) * float(item[0]['quantity'])
        else:
            item[0]['total_price'] = float(item[0]['price']) * float(item[0]['quantity'])
        list_products.append(item[0])

    products = {'products': list_products}

    pdf = render_to_pdf('shopping_history_pdf.html', products)
    return HttpResponse(pdf, content_type='application/pdf')


# def get(request):
#     cart = ShoppingCart.objects.all()
#     data = {
#         'count': cart.count(),
#         'empleados': cart
#     }
#     pdf = render_to_pdf('home/lista.html', data)
#     return HttpResponse(pdf, content_type='application/pdf')