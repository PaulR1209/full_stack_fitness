from django.shortcuts import render, redirect, reverse
from django.views import View
from django.conf import settings
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


class CheckoutView(View):
    def post(self, request, *args, **kwargs):
        membership_type = request.POST.get("membership_type")

        products = {
            "bronze": "price_1QApgeRo4WFpkduhqIGQ6dru",
            "silver": "price_1QAphIRo4WFpkduh51iLJTj7",
            "gold": "price_1QAphoRo4WFpkduhm7zZ5nMs",
        }

        if membership_type not in products:
            return redirect("membership")

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": products[membership_type],
                    "quantity": 1,
                }
            ],
            mode="subscription",
            success_url=request.build_absolute_uri(reverse("success")),
            cancel_url=request.build_absolute_uri(reverse("membership")),
        )

        return redirect(session.url, code=303)


class SuccessView(View):
    def get(self, request):
        membership_type = request.GET.get("membership_type", "Unknown Membership")

        return render(
            request, "checkout/success.html", {"membership_type": membership_type}
        )


class CancelView(View):
    def get(self, request):
        return render(request, "checkout/cancel.html")
