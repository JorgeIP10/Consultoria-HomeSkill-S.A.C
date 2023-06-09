from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives
import GoShop.settings as settings
from .models import UserProfile
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
            UserProfile.objects.filter(user_id=user.id).update(password=request.POST['password1'])
            
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