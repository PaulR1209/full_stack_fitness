from django.shortcuts import render, redirect, reverse
from django.views import View
from django.conf import settings
import stripe
from .models import Membership, Order
from django.utils import timezone
from dateutil.relativedelta import relativedelta

stripe.api_key = settings.STRIPE_SECRET_KEY


class CheckoutView(View):
    def post(self, request, *args, **kwargs):
        membership_type = request.POST.get("membership_type")

        products = {
            "Bronze": "price_1QApgeRo4WFpkduhqIGQ6dru",
            "Silver": "price_1QAphIRo4WFpkduh51iLJTj7",
            "Gold": "price_1QAphoRo4WFpkduhm7zZ5nMs",
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
            success_url=request.build_absolute_uri(reverse("success"))
            + f"?membership_type={membership_type}",
            cancel_url=request.build_absolute_uri(reverse("membership")),
        )

        return redirect(session.url, code=303)


class SuccessView(View):
    def get(self, request):
        membership_type = request.GET.get("membership_type", "Unknown Membership")

        if request.user.is_authenticated:
            membership = Membership.objects.filter(
                membership_type__iexact=membership_type
            ).first()
            if membership:
                order = Order.objects.create(
                    user=request.user,
                    membership=membership,
                    full_name=request.user.get_full_name(),
                    email=request.user.email,
                    is_paid=True,
                    last_renewed=timezone.now(),
                )
                order.next_renewal = order.last_renewed + relativedelta(months=1)
                order.save()

                return render(
                    request,
                    "checkout/success.html",
                    {"membership_type": membership_type},
                )

        return redirect("membership")


class CancelView(View):
    def get(self, request):
        return render(request, "checkout/cancel.html")
