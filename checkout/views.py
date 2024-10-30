import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.shortcuts import render
from django.contrib import messages
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from .models import Membership, Order

stripe.api_key = settings.STRIPE_SECRET_KEY


class Checkout(View):
    def post(self, request, *args, **kwargs):
        membership_price_map = {
            "Bronze": "price_1QApgeRo4WFpkduhqIGQ6dru",
            "Silver": "price_1QAphIRo4WFpkduh51iLJTj7",
            "Gold": "price_1QAphoRo4WFpkduhm7zZ5nMs",
        }

        selected_membership = request.POST.get("membership_type")
        membership_price_id = membership_price_map.get(selected_membership)

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                mode="subscription",
                line_items=[
                    {
                        "price": membership_price_id,
                        "quantity": 1,
                    }
                ],
                success_url=f"http://localhost:8000/checkout/success/?session_id={{CHECKOUT_SESSION_ID}}",
                cancel_url="http://localhost:8000/membership/",
                customer_email=request.user.email,
            )
            return redirect(checkout_session.url)
        except Exception as e:
            print(f"Error creating checkout session: {e}")
            messages.error(request, f"Checkout error: {str(e)}")
            return redirect("error")


class CheckoutSuccess(View):
    def get(self, request, *args, **kwargs):
        session_id = request.GET.get("session_id")

        try:
            checkout_session = stripe.checkout.Session.retrieve(session_id)

            line_items = stripe.checkout.Session.list_line_items(session_id)

            if line_items.data:
                price_id = line_items.data[0]["price"]["id"]
                customer = stripe.Customer.retrieve(checkout_session.customer)
                membership_instance = Membership.objects.get(stripe_price_id=price_id)

                Order.objects.create(
                    user=request.user,
                    full_name=customer.get("name"),
                    email=request.user.email,
                    membership=membership_instance,
                    created_at=timezone.now(),
                    last_renewed=timezone.now(),
                    next_renewal=timezone.now() + relativedelta(months=1),
                    is_paid=True,
                    subscription_id=checkout_session.id,
                    stripe_price_id=price_id,
                )

                return render(request, "checkout/success.html")
            else:
                raise Exception("No line items found.")

        except Exception as e:
            print(f"Error creating order: {e}")
            messages.error(request, f"Order error: {str(e)}")
            return redirect("error")


class CheckoutError(View):
    def get(self, request, *args, **kwargs):
        return render(request, "checkout/error.html")
