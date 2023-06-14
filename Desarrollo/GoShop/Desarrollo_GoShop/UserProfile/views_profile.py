from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .utils import render_to_pdf
from ShoppingCart.shop_cart import ShopCart
from Ventas_Retail.models import Product
import base64

@login_required                
def user_profile(request):
    if request.method == 'GET':
        return render(request, 'user_profile.html')
    else:
        names = {'Kitchen':'kitchen', 'Bathroom':'bathroom', 'Bedroom':'bedroom','Decor':'decor'}
        try:
            product = Product.objects.get(name=request.POST['search'])
            return redirect('description', view_name=names[product.category_id], product_id=product.id)
        except:
            return redirect('description', view_name='kitchen', product_id=0)

@login_required                
def user_config(request):
    if request.method == 'GET':
        return render(request, 'user_config.html')
    else:
        if 'button-search' in request.POST:
            names = {'Kitchen':'kitchen', 'Bathroom':'bathroom', 'Bedroom':'bedroom','Decor':'decor'}
            try:
                product = Product.objects.get(name=request.POST['search'])
                return redirect('description', view_name=names[product.category_id], product_id=product.id)
            except:
                return redirect('description', view_name='kitchen', product_id=0)
        elif 'confirm-username' in request.POST:
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

def shopping_history(request):
    if request.method == 'GET':
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
                    article['total_price'] = round(float(article['sale_price']) * float(article['quantity']), 2)
                    cart_amount += article['total_price']
                else:
                    article['total_price'] = round(float(article['price']) * float(article['quantity']), 2)
                    cart_amount += article['total_price']

                if cont_products_quantity != 1:
                    article['rows_quantity'] = len(item['products'])
                    cont_products_quantity += 1
                
                cont_rows += 1
                if cont_rows == len(item['products']):
                    article['new_row'] = True
                    article['cart_amount'] = round(cart_amount, 2)
                    total_amount += cart_amount

                list_products.append(article)

        products = {'products': list_products, 'total_amount': round(total_amount, 2)}

        pdf = render_to_pdf('shopping_history_pdf.html', products)
        pdf_data_base64 = base64.b64encode(pdf).decode('utf-8')
        return render(request, 'shopping_history.html', {'pdf': pdf_data_base64})
    else:
        names = {'Kitchen':'kitchen', 'Bathroom':'bathroom', 'Bedroom':'bedroom','Decor':'decor'}
        try:
            product = Product.objects.get(name=request.POST['search'])
            return redirect('description', view_name=names[product.category_id], product_id=product.id)
        except:
            return redirect('description', view_name='kitchen', product_id=0)