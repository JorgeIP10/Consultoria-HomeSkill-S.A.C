from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import UserProfile, PaymentCard
from django.http import JsonResponse

@login_required                
def user_profile(request):
    return render(request, 'user_profile.html')

@login_required                
def user_config(request):
    user = list(UserProfile.objects.filter(user_id=request.user.id).values())
    return render(request, 'user_config.html', {'user': user[0]})

def change_username(request, username):
    userObject = User.objects.get(username=request.user.username)
    userObject.username = username
    userObject.save()
    user = list(UserProfile.objects.filter(username=username).values())
    return JsonResponse({'username': user[0]['username']})

def change_password(request):
    if request.method == 'POST':
        new_password = request.POST['new-password']
        
        userObject = User.objects.get(password=request.user.password)
        userObject.set_password(new_password)
        userObject.save()
        user = authenticate(username=request.user.username, password=new_password)
        login(request, user)

        user = UserProfile.objects.get(user_id=request.user.id)
        user.password = new_password
        user.save()
        return JsonResponse({})

@login_required                
def user_payment(request):
    cards = PaymentCard.objects.filter(owner_id=request.user.id)
    dates = {'months': ['--', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'],
            'years': ['----', 2024, 2025, 2026, 2027, 2028, 2029, 2030, 2031, 2032, 2033, 2034]}
    if request.method == 'GET':
        return render(request, 'user_payment.html', {'cards': cards, 'dates': dates})
        
def add_payment_method(request):
    if request.method == 'POST':
        try:
            PaymentCard.objects.get(owner_id=request.user.id, number=request.POST['card'])
            return JsonResponse({'data': {'error': 'No se puede agregar la misma tarjeta.'}})
        except:
            PaymentCard.objects.create(owner_id=request.user.id, number=request.POST['card'],
            expiration_month=request.POST['select-month'],
            expiration_year=request.POST['select-year'],
            cvv=request.POST['cvv'])

            new_card = list(PaymentCard.objects.filter(owner_id=request.user.id, number=request.POST['card']).values())
            return JsonResponse({'data': {'message': 'La tarjeta ha sido agregada exitosamente.', 'card': new_card[0]}})

def remember_payment_method(request):
    if request.method == 'POST':
        try:
            card_remembered = PaymentCard.objects.get(owner_id=request.user.id, remembered=True)
            if (card_remembered.id != request.POST['remember-card'] and
                card_remembered.owner_id == request.user.id):
                card_remembered.remembered = False
                card_remembered.save()

                new_card_remembered = PaymentCard.objects.get(id=request.POST['remember-card'])
                new_card_remembered.remembered = True
                new_card_remembered.save()
            return JsonResponse({'data': {'message': 'La tarjeta ha sido recordada.'}})
        except:
            PaymentCard.objects.filter(owner_id=request.user.id, id=request.POST['remember-card']).update(remembered=True)
            return JsonResponse({'data': {'message_without_remember': 'La tarjeta ha sido recordada.'}})