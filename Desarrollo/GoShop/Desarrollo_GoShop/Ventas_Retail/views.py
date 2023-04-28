from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
import GoShop.settings as settings
from .models import Product
from django.http import JsonResponse

# Create your views here.
def signup(request):
    if request.method == 'GET':
        if request.user.is_anonymous:
            return render(request, 'register.html')
        else:
            return redirect('shop')
    else:
        try:
            user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'], email=request.POST['email'])
            email = request.POST['email']
            template = get_template('register_email.html')
            content = template.render({'username': request.POST['username']})

            message = EmailMultiAlternatives("¡Bienvenido a GoShop!",
                                f"Bienvenido, {request.POST['username']}, te has registrado correctamente a nuestra tienda virtual.",
                                settings.EMAIL_HOST_USER,
                                [email])
            message.attach_alternative(content, 'text/html')
            user.save()
            login(request, user)
            message.send()
            return redirect('shop')
        except IntegrityError:
            return render(request, 'register.html', {'username': request.POST['username'], 'error': 'El usuario ya existe.'})

def signin(request):
    if request.method == 'GET':
        if request.user.is_anonymous:
            return render(request, 'login.html')
        else:
            return redirect('shop')
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {'error': 'Usuario y/o contraseña incorrecto(s).'})
        else:
            login(request, user)
            return redirect('shop')

@login_required
def signout(request):
    logout(request)
    return redirect('shop')

def shop(request):
    if request.method == 'GET':
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

def get_products(request, text):
    products = list(Product.objects.values())
    names_products = []
    for product in products:
        if product['name'].lower().startswith(text.lower()):
            names_products.append(product['name'])

    data = {'products': names_products}
    return JsonResponse(data)

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
        if request.user.is_anonymous:
            return redirect('signin')
        else:
            names = {'Kitchen':'kitchen', 'Bathroom':'bathroom', 'Bedroom':'bedroom', 'Decor':'decor'}
            if 'button-search' in request.POST:
                try:
                    product = Product.objects.get(name=request.POST['search'])
                    return redirect('description', view_name=names[product.category_id], product_id=product.id)
                except:
                    return redirect('description', view_name='offers', product_id=0)
                
            elif 'see-description' in request.POST:
                try:
                    product = Product.objects.get(id=request.POST['product_id'])
                    print(product.category_id)
                    return redirect('description', view_name=names[product.category_id], product_id=product.id)
                except:
                    return redirect('description',  view_name='offers', product_id=0)