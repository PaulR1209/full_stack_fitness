from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm
import stripe

# Create your views here.


stripe.api_key = settings.STRIPE_KEYS["SECRET_KEY"]

@login_required
def checkout(request):
    if request.method == "POST":
        form = OrderForm(request.POST)

        if form.is_valid():
            try:
                amount = 500
                payment_intent = stripe.PaymentIntent.create(
                    amount=amount,
                    currency="gbp",
                    payment_method_types=["card"],
                )
            
                order = form.save(commit=False)
                order.user = request.user
                order.stripe_pid = payment_intent.id
                order.save()
                messages.success(request, "Payment successful! You are now a member!")
                return redirect("membership")
        
            except Exception as e:
                messages.error(request, "An error occurred while processing your payment: " + str(e))
                return render(request, "checkout/checkout.html", {"form": form})
    else:
        form = OrderForm()

    return render(request, "checkout/checkout.html", {"form": form})
    