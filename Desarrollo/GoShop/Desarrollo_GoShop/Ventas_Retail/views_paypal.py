from django.urls import reverse
from django.shortcuts import render
from .forms import CustomPayPalPaymentsForm
from django.conf import settings
import uuid

def paypal(request):

    # What you want the button to do.
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": "0.10",
        "item_name": "name of the item",
        "quantity": 10,
        "add": 1,
        "invoice": str(uuid.uuid4()),
        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('successful_payment')),
        "cancel_return": request.build_absolute_uri(reverse('payment_error')),
        # "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    form = CustomPayPalPaymentsForm(initial=paypal_dict)
    context = {"form": form}
    return render(request, "paypal.html", context)

def payment_error(request):
    return render(request, 'payment_error.html')

def successful_payment(request):
    return render(request, 'successful_payment.html')