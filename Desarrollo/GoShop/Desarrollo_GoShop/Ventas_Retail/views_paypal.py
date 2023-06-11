from django.urls import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm

def paypal(request):

    # What you want the button to do.
    paypal_dict = {
        "business": "correo@business.example.com",
        "amount": "1.00",
        "item_name": "name of the item",
        "invoice": "unique-invoice-id",
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('successful_payment')),
        "cancel_return": request.build_absolute_uri(reverse('payment_error')),
        # "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "paypal.html", context)

def payment_error(request):
    return render(request, 'payment_error.html')

def successful_payment(request):
    return render(request, 'successful_payment.html')