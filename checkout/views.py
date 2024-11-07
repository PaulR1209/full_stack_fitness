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
    """View to handle the checkout process for memberships."""
    def post(self, request, *args, **kwargs):
        # Map membership types to Stripe price IDs
        membership_price_map = {
            "Bronze": "price_1QApgeRo4WFpkduhqIGQ6dru",
            "Silver": "price_1QAphIRo4WFpkduh51iLJTj7",
            "Gold": "price_1QAphoRo4WFpkduhm7zZ5nMs",
        }
        # Get the selected membership type
        selected_membership = request.POST.get("membership_type")
        # Get the Stripe price ID for the selected membership
        membership_price_id = membership_price_map.get(selected_membership)

        try:
            # Create a new checkout session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                mode="subscription",
                line_items=[
                    {
                        "price": membership_price_id,
                        "quantity": 1,
                    }
                ],
                # Set the success and cancel URLs
                success_url=(
                    f"https://full-stack-fitness-a73d59e5c070.herokuapp.com/"
                    f"checkout/success/"
                    f"{{CHECKOUT_SESSION_ID}}"
                    ),
                cancel_url=request.build_absolute_uri("/membership/"),
                customer_email=request.user.email,
            )

            return redirect(checkout_session.url)
        except ValueError as e:
            messages.error(request, f"Error: {str(e)}")
        except stripe.error.CardError:
            messages.error(
                request,
                "Your payment method was declined."
                "Please check your payment details.",
            )
        except stripe.error.RateLimitError:
            messages.error(
                request, "We're experiencing high traffic."
                "Please try again later."
            )
        except stripe.error.InvalidRequestError:
            messages.error(
                request,
                "There was an error with your request."
                "Please check your input.",
            )
        except Exception as e:
            messages.error(request, "An unexpected error occurred."
                           "Please try again.")
            print(f"Unexpected error: {e}")

        return redirect("error")


class CheckoutSuccess(View):
    """View to handle the success page after a successful checkout."""
    def get(self, request, *args, **kwargs):
        session_id = self.kwargs["session_id"]
        try:
            # Retrieve the checkout session
            checkout_session = stripe.checkout.Session.retrieve(session_id)
            # Retrieve the line items from the checkout session
            line_items = stripe.checkout.Session.list_line_items(session_id)

            if line_items.data:
                price_id = line_items.data[0]["price"]["id"]
                subscription_id = checkout_session.subscription
                customer_id = checkout_session.customer
                customer = stripe.Customer.retrieve(checkout_session.customer)
                membership_instance = Membership.objects.get(
                    stripe_price_id=price_id
                    )
                price = Decimal(
                    line_items.data[0]["price"]["unit_amount"] / 100
                    )

                session_email = checkout_session.customer_details.email
                # Check if the session email matches the user email
                if session_email != request.user.email:
                    messages.error(
                        request, "This session does not belong to your account"
                    )
                    return redirect("membership")

                # Check if the user already has an active membership
                if Order.objects.filter(
                    user=request.user, subscription_id=subscription_id
                ).exists():
                    messages.warning(
                        request, "You have already purchased this membership."
                    )
                    return redirect("membership")

                existing_orders = Order.objects.filter(user=request.user)

                # Check for any expired orders and delete them
                if existing_orders.exists():
                    for order in existing_orders:
                        if order.is_expired:
                            order.delete()

                # Add the new order to the database
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
                    session_id=session_id,
                    customer_id=customer_id,
                    membership_price=price,
                )

                return render(request, "checkout/success.html")
            else:
                raise Exception("No line items found.")

        except stripe.error.StripeError as e:
            messages.error(
                request,
                "There was a problem processing your payment."
                "Please try again.",
            )
            print(f"Stripe error: {str(e)}")

        except Membership.DoesNotExist:
            messages.error(
                request, "The selected membership type is no longer available."
            )
            print("Membership does not exist.")

        except Order.DoesNotExist:
            messages.error(
                request, "Unable to find your order. Please contact support."
            )
            print("Order does not exist.")

        except Exception as e:
            messages.error(request, f"An unexpected error occurred: {str(e)}")
            print(f"Unexpected error: {e}")

        return redirect("error")


class CheckoutError(View):
    """View to handle the error page after an unsuccessful checkout."""
    def get(self, request, *args, **kwargs):
        error_message = messages.get_messages(request)
        return render(
            request, "checkout/error.html", {"error_message": error_message})


class CancelMembership(View):
    """View to handle the cancellation of a membership."""
    def post(self, request, *args, **kwargs):
        # Get the user's order
        try:
            user_order = Order.objects.filter(
                user=request.user, is_cancelled=False
            ).last()
            if user_order and user_order.subscription_id:
                print(
                    f"Attempting to cancel subscription ID:"
                    f"{user_order.subscription_id}"
                )

                # Cancel the subscription at the end of the billing period
                stripe.Subscription.modify(
                    user_order.subscription_id, cancel_at_period_end=True
                )
                # Update the database
                user_order.cancellation_date = user_order.next_renewal
                user_order.expiry_date = user_order.next_renewal
                user_order.next_renewal = None
                user_order.is_cancelled = True
                user_order.save()

            else:
                messages.error(request, "No active membership found.")
        except Order.DoesNotExist:
            messages.error(request, "Order not found.")
        except Exception as e:
            print(f"Error cancelling membership: {e}")
            messages.error(request, f"Error cancelling membership: {str(e)}")

        return redirect("manage")


class ReactivateMembership(View):
    """View to handle the reactivation of a cancelled membership."""
    def post(self, request, *args, **kwargs):
        try:
            # Get the user's order
            user_order = Order.objects.filter(
                user=request.user, is_cancelled=True
            ).last()
            if user_order and user_order.subscription_id:
                print(
                    f"Attempting to reactivate subscription ID:"
                    f"{user_order.subscription_id}"
                )

                # Reactivate the subscription
                stripe.Subscription.modify(
                    user_order.subscription_id, cancel_at_period_end=False
                )

                # Update the database
                user_order.next_renewal = user_order.cancellation_date
                user_order.cancellation_date = None
                user_order.expiry_date = None
                user_order.is_cancelled = False
                user_order.save()

                messages.success(
                    request, "Membership reactivated successfully.")
            else:
                messages.error(request, "No cancelled membership found.")
        except Order.DoesNotExist:
            messages.error(request, "Order not found.")
        except Exception as e:
            print(f"Error reactivating membership: {e}")
            messages.error(request, f"Error reactivating membership: {str(e)}")

        return redirect("manage")


class ChangeMembership(View):
    """View to handle the changing of a membership."""
    def post(self, request, *args, **kwargs):
        # Get the selected membership type
        selected_membership = request.POST.get("membership_type")

        try:
            # Get the user's order
            user_order = Order.objects.filter(
                user=request.user, is_cancelled=False
            ).last()
            if user_order:
                subscription_id = user_order.subscription_id
                subscription = stripe.Subscription.retrieve(subscription_id)

                # Map membership types to Stripe price IDs
                membership_price_map = {
                    "Bronze": ("price_1QApgeRo4WFpkduhqIGQ6dru", 25),
                    "Silver": ("price_1QAphIRo4WFpkduh51iLJTj7", 35),
                    "Gold": ("price_1QAphoRo4WFpkduhm7zZ5nMs", 50),
                }

                # Get the current membership and price
                current_membership = Membership.objects.get(
                    stripe_price_id=user_order.stripe_price_id
                )
                current_price_id = user_order.stripe_price_id
                new_price_id = membership_price_map.get(selected_membership)[0]

                current_price_amount = membership_price_map[
                    current_membership.membership_type
                ][1]
                # Get the new membership price
                new_price_amount = membership_price_map[selected_membership][1]

                # Check whether the user is upgrading or downgrading
                if new_price_id and new_price_id != current_price_id:
                    new_membership = Membership.objects.get(
                        stripe_price_id=new_price_id
                    )
                    is_upgrade = new_price_amount > current_price_amount
                    is_downgrade = new_price_amount < current_price_amount

                    subscription_item_id = (
                        subscription["items"]["data"][0]["id"]
                        )

                    # Upgrade the subscription on stripe
                    if is_upgrade:
                        stripe.Subscription.modify(
                            subscription_id,
                            items=[{
                                "id": subscription_item_id,
                                "price": new_price_id
                                }],
                            billing_cycle_anchor="unchanged",
                            proration_behavior="create_prorations",
                        )

                        # Update the database
                        user_order.membership = new_membership
                        user_order.pending_membership = None
                        user_order.previous_membership_price = (
                            current_price_amount
                            )
                        user_order.stripe_price_id = new_price_id
                        user_order.membership_price = new_price_amount
                        user_order.has_changed = True
                        user_order.save()

                        proration_amount = user_order.proration_amount
                        prorated_amount = round(proration_amount, 2)

                        messages.success(
                            request,
                            f"Your membership has been upgraded to"
                            f"{selected_membership}. You will be charged"
                            f"£{prorated_amount} plus the new membership fee"
                            "at the next renewal date.",
                        )

                    # Downgrade the subscription on stripe
                    elif is_downgrade:
                        stripe.Subscription.modify(
                            subscription_id,
                            items=[{
                                "id": subscription_item_id,
                                "price": new_price_id
                                }],
                            proration_behavior="none",
                            billing_cycle_anchor="unchanged",
                            cancel_at_period_end=False,
                        )

                        # Update the database
                        user_order.pending_membership = new_membership
                        user_order.pending_membership_price = new_price_amount
                        user_order.stripe_price_id = new_price_id
                        user_order.has_changed = True
                        user_order.save()

                        messages.success(
                            request,
                            f"Your membership will be downgraded to"
                            f"{selected_membership} at the next renewal date.",
                        )

                else:
                    messages.info(
                        request, "You are already on this membership plan."
                        )
            else:
                messages.error(request, "No active membership found.")
        except Exception as e:
            print(f"Error changing membership: {e}")
            messages.error(request, f"Error changing membership: {str(e)}")

        return redirect("manage")


def check_and_update_payment_status(request, user, subscription_id):
    """Function to check and update the payment status of a subscription."""
    try:
        subscription = stripe.Subscription.retrieve(subscription_id)
        user_order = Order.objects.get(
            user=user, subscription_id=subscription_id
            )
        today = timezone.now()

        if subscription["cancel_at_period_end"]:
            user_order.is_cancelled = True
            user_order.expiry_date = user_order.next_renewal
            messages.info(
                request,
                "Your membership has been cancelled"
                "and will expire at the end of the current billing period.",
            )
        elif subscription["status"] == "active":
            user_order.is_paid = True
        elif subscription["status"] == "past_due":
            user_order.is_paid = False
            messages.warning(
                request,
                "Your payment failed. Please repay within 14 days"
                "from the start of the billing cycle,"
                "by updating your payment method, to avoid cancellation.",
            )
        elif subscription["status"] == "canceled":
            user_order.is_cancelled = True
            user_order.expiry_date = today
            user_order.is_expired = True
            messages.info(
                request,
                "Your membership has been cancelled."
                "Please purchase a new membership.",
            )

        user_order.save()

        return "Payment status updated successfully."

    except Order.DoesNotExist:
        return "Order not found."
    except Exception as e:
        return f"Error updating payment status: {str(e)}"


class UpdatePaymentMethod(View):
    """View to handle the updating of a payment method."""
    def post(self, request, *args, **kwargs):
        try:
            user_order = Order.objects.filter(
                user=request.user, is_cancelled=False
            ).last()
            if not user_order:
                messages.error(request, "No active membership found.")
                return redirect("manage")

            customer_id = user_order.customer_id

            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                customer=customer_id,
                mode="setup",
                success_url=request.build_absolute_uri(
                    "/checkout/payment-update-success/"
                    ),
                cancel_url=request.build_absolute_uri("/cancel/"),
            )

            return redirect(session.url)
        except Exception as e:
            messages.error(request, f"Error updating payment method: {str(e)}")
            return redirect("manage")


class PaymentUpdateSuccess(View):
    """View to handle the success page after a successful payment update."""
    def get(self, request, *args, **kwargs):
        messages.success(
            request, "Your payment method has been successfully updated!"
            )
        return render(request, "checkout/update_payment_success.html")
