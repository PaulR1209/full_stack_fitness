import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.views import View
from django.shortcuts import render
from django.contrib import messages

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
                success_url = "http://localhost:8000/checkout/success/",
                cancel_url = "http://localhost:8000/membership/",

                customer_email=request.user.email,
            )
            return redirect(checkout_session.url)
        except Exception as e:
            print(f"Error creating checkout session: {e}")
            messages.error(request, f"Checkout error: {str(e)}")
            return redirect("error")
        

class CheckoutSuccess(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'checkout/success.html')
    

class CheckoutError(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'checkout/error.html')

