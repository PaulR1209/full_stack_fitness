import stripe
from django.conf import settings
from django.shortcuts import redirect, render
from django.views import View
from django.contrib import messages
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from .models import Membership, Order
from decimal import Decimal

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
                subscription_id = checkout_session.subscription
                customer = stripe.Customer.retrieve(checkout_session.customer)
                membership_instance = Membership.objects.get(stripe_price_id=price_id)
                price = Decimal(line_items.data[0]["price"]["unit_amount"] / 100)

                Order.objects.create(
                    user=request.user,
                    full_name=customer.get("name"),
                    email=request.user.email,
                    membership=membership_instance,
                    created_at=timezone.now(),
                    last_renewed=timezone.now(),
                    is_paid=True,
                    subscription_id=subscription_id,
                    stripe_price_id=price_id,
                    membership_price=price,
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


class CancelMembership(View):
    def post(self, request, *args, **kwargs):
        try:
            user_order = Order.objects.filter(
                user=request.user, is_cancelled=False
            ).last()
            if user_order and user_order.subscription_id:
                print(
                    f"Attempting to cancel subscription ID: {user_order.subscription_id}"
                )

                stripe.Subscription.modify(
                    user_order.subscription_id, cancel_at_period_end=True
                )

                user_order.cancellation_date = user_order.next_renewal
                user_order.next_renewal = None
                user_order.is_cancelled = True
                user_order.save()

                cancellation_date = (
                    user_order.cancellation_date.strftime("%d %B %Y")
                    if user_order.cancellation_date
                    else "unknown"
                )
                messages.success(
                    request,
                    f"Membership cancelled successfully. Your membership will expire on {cancellation_date}.",
                )
            else:
                messages.error(request, "No active membership found.")
        except Order.DoesNotExist:
            messages.error(request, "Order not found.")
        except Exception as e:
            print(f"Error cancelling membership: {e}")
            messages.error(request, f"Error cancelling membership: {str(e)}")

        return redirect("manage")


class ReactivateMembership(View):
    def post(self, request, *args, **kwargs):
        try:
            user_order = Order.objects.filter(
                user=request.user, is_cancelled=True
            ).last()
            if user_order and user_order.subscription_id:
                print(
                    f"Attempting to reactivate subscription ID: {user_order.subscription_id}"
                )

                stripe.Subscription.modify(
                    user_order.subscription_id, cancel_at_period_end=False
                )

                user_order.next_renewal = user_order.cancellation_date
                user_order.cancellation_date = None
                user_order.is_cancelled = False
                user_order.save()

                messages.success(request, "Membership reactivated successfully.")
            else:
                messages.error(request, "No cancelled membership found.")
        except Order.DoesNotExist:
            messages.error(request, "Order not found.")
        except Exception as e:
            print(f"Error reactivating membership: {e}")
            messages.error(request, f"Error reactivating membership: {str(e)}")

        return redirect("manage")


class ChangeMembership(View):
    def post(self, request, *args, **kwargs):
        selected_membership = request.POST.get("membership_type")

        try:
            user_order = Order.objects.filter(
                user=request.user, is_cancelled=False
            ).last()
            if user_order:
                subscription_id = user_order.subscription_id
                subscription = stripe.Subscription.retrieve(subscription_id)

                membership_price_map = {
                    "Bronze": ("price_1QApgeRo4WFpkduhqIGQ6dru", 2500),
                    "Silver": ("price_1QAphIRo4WFpkduh51iLJTj7", 3500),
                    "Gold": ("price_1QAphoRo4WFpkduhm7zZ5nMs", 5000),
                }

                current_membership = Membership.objects.get(stripe_price_id=user_order.stripe_price_id)
                current_price_id = user_order.stripe_price_id
                new_price_id = membership_price_map.get(selected_membership)[0]

                current_price_amount = membership_price_map[current_membership.membership_type][1]
                new_price_amount = membership_price_map[selected_membership][1]

                if new_price_id and new_price_id != current_price_id:
                    new_membership = Membership.objects.get(stripe_price_id=new_price_id)
                    is_upgrade = (new_price_amount > current_price_amount)
                    is_downgrade = (new_price_amount < current_price_amount)

                    subscription_item_id = subscription['items']['data'][0]['id']

                    if is_upgrade:
                        stripe.Subscription.modify(
                            subscription_id,
                            items=[{'id': subscription_item_id, 'price': new_price_id}],
                            billing_cycle_anchor="unchanged",
                            proration_behavior="create_prorations",
                        )

                        user_order.membership = new_membership
                        user_order.pending_membership = None
                        user_order.save()

                        messages.success(
                            request,
                            f"Your membership has been upgraded to {selected_membership}.",
                        )

                    elif is_downgrade:
                        stripe.Subscription.modify(
                            subscription_id,
                            items=[{'id': subscription_item_id, 'price': new_price_id}],
                            proration_behavior="none",
                            billing_cycle_anchor="unchanged",
                            cancel_at_period_end=False,
                        )

                        user_order.pending_membership = new_membership
                        user_order.save()

                        messages.success(
                            request,
                            f"Your membership will be downgraded to {selected_membership} at the next renewal date.",
                        )

                else:
                    messages.info(request, "You are already on this membership plan.")
            else:
                messages.error(request, "No active membership found.")
        except Exception as e:
            print(f"Error changing membership: {e}")
            messages.error(request, f"Error changing membership: {str(e)}")

        return redirect("manage")


def check_and_update_payment_status(user, subscription_id):
    try:
        subscription = stripe.Subscription.retrieve(subscription_id)

        is_paid = subscription['status'] == "active"

        user_order = Order.objects.get(user=user, subscription_id=subscription_id)
        user_order.is_active = is_paid
        user_order.is_paid = is_paid
        user_order.save()

        return 'Payment status updated successfully.'
    
    except Order.DoesNotExist:
        return 'Order not found.'
    except Exception as e:
        return f'Error updating payment status: {str(e)}'

        