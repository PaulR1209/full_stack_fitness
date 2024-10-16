from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm
import stripe
from membership.models import Membership


@login_required
def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    # Check if there is an item in the cart
    membership_id = request.session.get("cart_id")
    membership = None
    grand_total = 0
    item_count = 0

    if membership_id:
        membership = get_object_or_404(Membership, id=membership_id)
        grand_total = (
            membership.price
        )  # Assuming `price` is a field in your Membership model
        item_count = 1  # Since you only allow one membership

    if item_count == 0:
        messages.error(request, "There is nothing in your cart at the moment")
        return redirect("memberships")

    stripe_total = round(grand_total * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    order_form = OrderForm()
    template = "checkout/checkout.html"
    context = {
        "order_form": order_form,
        "stripe_public_key": stripe_public_key,
        "client_secret": intent.client_secret,
        "membership": membership,  # Pass the membership details to the template
        "grand_total": grand_total,  # Pass the grand total to the template
    }

    return render(request, template, context)
