from django.shortcuts import render, redirect, reverse
from django.views import View
from django.conf import settings
import stripe
from .models import Membership, Order
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.contrib import messages

# Set the Stripe secret key from the Django settings
stripe.api_key = settings.STRIPE_SECRET_KEY


class CheckoutView(View):
    """View to handle the checkout process for membership subscriptions."""

    def post(self, request, *args, **kwargs):
        membership_type = request.POST.get("membership_type")

        # Mapping of membership types to Stripe product prices
        products = {
            "Bronze": "price_1QApgeRo4WFpkduhqIGQ6dru",
            "Silver": "price_1QAphIRo4WFpkduh51iLJTj7",
            "Gold": "price_1QAphoRo4WFpkduhm7zZ5nMs",
        }

        if membership_type not in products:
            return redirect("membership")

        # Create a new Stripe checkout session for subscription payment
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
            + f"?membership_type={membership_type}&session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=request.build_absolute_uri(reverse("membership")),
        )

        # Redirect to the Stripe checkout page
        return redirect(session.url, code=303)


class SuccessView(View):
    """View to handle the success page after a successful subscription."""

    def get(self, request):
        # Retrieve session ID and membership type from the URL parameters
        session_id = request.GET.get("session_id")
        membership_type = request.GET.get("membership_type", "Unknown Membership")

        if session_id:
            # Retrieve the Stripe checkout session using the session ID
            session = stripe.checkout.Session.retrieve(session_id)
            subscription_id = session.subscription
            customer_id = session.customer

            # Process the order if the user is authenticated
            if request.user.is_authenticated:
                membership = Membership.objects.filter(
                    membership_type__iexact=membership_type
                ).first()

                if membership:
                    try:
                        # Retrieve the customer details from Stripe
                        customer = stripe.Customer.retrieve(customer_id)
                        full_name = customer.name

                        # Create a new order in the database
                        order = Order.objects.create(
                            user=request.user,
                            membership=membership,
                            full_name=full_name,
                            email=request.user.email,
                            is_paid=True,
                            last_renewed=timezone.now(),
                            subscription_id=subscription_id,
                            stripe_price_id=membership.stripe_price_id,
                        )

                        # Calculate the next renewal date after creating the order
                        order.calculate_next_renewal()
                        order.save()

                        return render(
                            request,
                            "checkout/success.html",
                            {"membership_type": membership_type},
                        )
                    # Handle any errors that occur during order processing
                    except stripe.error.StripeError as e:
                        messages.error(request, f"Error retrieving customer: {str(e)}")
                        return redirect("membership")

        return redirect("membership")


class MembershipStatusView(View):
    """View to check the membership renewal status."""

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("membership")

        # Retrieve the user's active order
        order = Order.objects.filter(user=request.user, is_cancelled=False).first()

        if order:
            now = timezone.now()
            if order.next_renewal < now:
                # Check Stripe for payment success
                try:
                    subscription = stripe.Subscription.retrieve(order.subscription_id)
                    if subscription.status == "active":
                        order.is_paid = True
                    else:
                        order.is_paid = False

                    order.save()

                    if not order.is_paid:
                        messages.warning(
                            request,
                            "Your renewal payment has failed. Please update your payment.",
                        )
                        return render(
                            request,
                            "checkout/membership_status.html",
                            {
                                "order": order,
                            },
                        )
                except stripe.error.StripeError as e:
                    messages.error(request, f"Error checking payment status: {str(e)}")

        return render(request, "checkout/membership_status.html", {"order": order})


class CancelConfirmationView(View):
    """View to display the cancellation confirmation page."""

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect("membership")
        return render(request, "checkout/cancel.html")


class CancelMembershipView(View):
    """View to handle the cancellation of a membership subscription."""

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("membership")

        # Retrieve the user's active order
        order = Order.objects.filter(user=request.user, is_cancelled=False).first()

        if order:
            try:
                # Modify the Stripe subscription to cancel at the end of the billing period
                stripe.Subscription.modify(
                    order.subscription_id, cancel_at_period_end=True
                )

                # Update order status in the database
                order.is_cancelled = True
                order.cancellation_date = (
                    order.next_renewal
                )  # Set the cancellation date
                order.next_renewal = None  # Remove the next renewal date
                order.save()

                messages.success(
                    request,
                    f"Your subscription has been canceled successfully. It will be active until {order.cancellation_date.strftime('%B %d, %Y')}.",
                )
            except stripe.error.StripeError as e:
                messages.error(request, f"Error canceling subscription: {str(e)}")

            return redirect("membership")

        messages.warning(request, "No active subscription found.")
        return redirect("membership")


class ReactivateMembershipView(View):
    """View to handle the reactivation of a canceled membership subscription."""

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("membership")

        # Retrieve the user's canceled order
        order = Order.objects.filter(
            user=request.user, is_cancelled=True, cancellation_date__gte=timezone.now()
        ).first()

        if order:
            try:
                # Modify the Stripe subscription to reactivate it
                stripe.Subscription.modify(
                    order.subscription_id, cancel_at_period_end=False
                )

                # Update order status in the database
                order.is_cancelled = False
                order.cancellation_date = None
                order.next_renewal = order.last_renewed + relativedelta(
                    months=1
                )  # Calculate the next renewal date
                order.save()

                messages.success(
                    request, "Your membership has been successfully reactivated."
                )
            except stripe.error.StripeError as e:
                messages.error(request, f"Error reactivating membership: {str(e)}")

            return redirect("manage")

        messages.warning(request, "No canceled membership found to reactivate.")
        return redirect("membership")


class ChangeMembershipView(View):
    """View to handle the change of membership subscription."""

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect("membership")

        # Retrieve the user's active order
        user_order = Order.objects.filter(user=request.user, is_cancelled=False).first()
        new_membership_type = request.POST.get("membership_type")
        new_membership = Membership.objects.get(membership_type=new_membership_type)

        if user_order and user_order.subscription_id:
            # Retrieve the Stripe subscription details
            stripe_subscription = stripe.Subscription.retrieve(
                user_order.subscription_id
            )
            current_membership_price = user_order.membership.price
            new_membership_price = new_membership.price
            remaining_days = (user_order.next_renewal - timezone.now()).days
            upgrade_price = (new_membership_price - current_membership_price) * (
                remaining_days / 30
            )

            # Check if the user is upgrading their membership
            if new_membership_price > current_membership_price:
                stripe.Subscription.modify(
                    stripe_subscription.id,
                    items=[
                        {
                            "id": stripe_subscription["items"]["data"][0].id,
                            "price": new_membership.stripe_price_id,
                        }
                    ],
                    proration_behavior="create_prorations",
                )
                user_order.membership = new_membership
                user_order.save()
                messages.success(
                    request,
                    f"You have successfully upgraded to the {new_membership_type} Membership.",
                )
                messages.info(
                    request,
                    f"An additional charge of £{upgrade_price:.2f} will be added to your next bill.",
                )

            # Check if the user is downgrading their membership
            else:
                stripe.Subscription.modify(
                    stripe_subscription.id,
                    items=[
                        {
                            "id": stripe_subscription["items"]["data"][0].id,
                            "price": new_membership.stripe_price_id,
                        }
                    ],
                    proration_behavior="none",
                    billing_cycle_anchor="unchanged",
                )
                user_order.pending_membership = new_membership
                user_order.cancellation_date = user_order.next_renewal
                user_order.save()
                next_renewal_date = user_order.next_renewal.strftime("%B %d, %Y")

                messages.success(
                    request,
                    f"You have successfully downgraded your membership to {new_membership_type}. Your membership will change on {next_renewal_date}.",
                )

            return redirect("membership")

        messages.warning(request, "No active subscription found.")
        return redirect("membership")


def update_memberships():
    """Update membership status based on renewal dates."""
    now = timezone.now()
    # Delete cancelled orders
    cancelled_orders = Order.objects.filter(
        is_cancelled=True, cancellation_date__lte=now
    )
    for order in cancelled_orders:
        order.delete()

    # Handle downgraded memberships for active orders
    active_orders = Order.objects.filter(is_cancelled=False, next_renewal__lte=now)
    for order in active_orders:
        if order.pending_membership:
            order.membership = order.pending_membership
            order.pending_membership = None
            order.cancellation_date = None
            order.last_renewed = order.next_renewal
            order.calculate_next_renewal()
            order.save()

    # Handle renewals for active memberships
    for order in active_orders:
        if order.next_renewal <= now:
            order.last_renewed = order.next_renewal
            order.calculate_next_renewal()
            order.save()
