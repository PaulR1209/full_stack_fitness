from django.shortcuts import render, redirect, reverse
from django.views import View
from django.conf import settings
import stripe

# Set your secret key
stripe.api_key = settings.STRIPE_SECRET_KEY


class CheckoutView(View):
    def post(self, request, *args, **kwargs):
        membership_type = request.POST.get("membership_type")

        # Define membership products and prices
        products = {
            "bronze": 2500,  # Price in pence (£25)
            "silver": 3500,  # Price in pence (£35)
            "gold": 5000,  # Price in pence (£50)
        }

        # Validate membership type
        if membership_type not in products:
            return redirect("membership")  # Redirect back if invalid

        # Create a new Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "gbp",
                        "product_data": {
                            "name": f"{membership_type.capitalize()} Membership",
                        },
                        "unit_amount": products[membership_type],
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url=request.build_absolute_uri(reverse("success")),  # Adjust URL as needed
            cancel_url=request.build_absolute_uri(reverse("membership")),
        )

        # Redirect to Stripe Checkout
        return redirect(session.url, code=303)


class SuccessView(View):
    def get(self, request):
        return render(request, "checkout/success.html")


class CancelView(View):
    def get(self, request):
        return render(request, "checkout/cancel.html")
