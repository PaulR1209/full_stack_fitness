from django.contrib import messages
from django.shortcuts import render
from .models import Membership
from checkout.models import Order
from checkout.views import update_memberships
from django.utils import timezone


def membership(request):
    """Display the membership page"""
    user_order = None
    if request.user.is_authenticated:
        # Get the user's most recent order
        user_order = Order.objects.filter(user=request.user).first()

        if user_order:
            # Check if the user's membership has expired by looking at the cancellation date
            if (
                user_order.is_cancelled
                and user_order.cancellation_date
                and user_order.cancellation_date < timezone.now()
            ):
                # Show the expiration message if the membership is cancelled and the cancellation date is in the past
                messages.warning(
                    request,
                    "Your membership has expired. Refresh the page to begin a new membership.",
                )

            # Check if the user is downgrading membership
            elif (
                user_order.pending_membership
                and user_order.next_renewal
                and user_order.next_renewal < timezone.now()
            ):
                messages.info(
                    request,
                    "Your membership has successfully been downgraded. Refresh the page to view changes.",
                )

    # Call the update_memberships() to clean up expired memberships
    update_memberships()

    # Retrieve membership types
    memberships = {
        "Bronze": Membership.objects.filter(membership_type="Bronze").first(),
        "Silver": Membership.objects.filter(membership_type="Silver").first(),
        "Gold": Membership.objects.filter(membership_type="Gold").first(),
    }

    # Get all orders for the user
    orders = Order.objects.filter(user=request.user)

    return render(
        request,
        "membership/membership.html",
        {
            "memberships": memberships,
            "user_order": user_order,
            "orders": orders,
        },
    )


def manage(request):
    """Display the manage membership page"""
    update_memberships()

    user_order = None
    if request.user.is_authenticated:
        user_order = (
            Order.objects.filter(user=request.user).order_by("-created_at").first()
        )

    # Retrieve membership types
    memberships = {
        "Bronze": Membership.objects.filter(membership_type="Bronze").first(),
        "Silver": Membership.objects.filter(membership_type="Silver").first(),
        "Gold": Membership.objects.filter(membership_type="Gold").first(),
    }

    context = {
        "user_order": user_order,
        "memberships": memberships,
    }

    return render(request, "membership/manage.html", context)


def change(request):
    """Display the change membership page"""
    update_memberships()

    user_order = None
    if request.user.is_authenticated:
        user_order = (
            Order.objects.filter(user=request.user).order_by("-created_at").first()
        )

    # Retrieve membership types
    memberships = {
        "Bronze": Membership.objects.filter(membership_type="Bronze").first(),
        "Silver": Membership.objects.filter(membership_type="Silver").first(),
        "Gold": Membership.objects.filter(membership_type="Gold").first(),
    }

    context = {
        "user_order": user_order,
        "memberships": memberships,
    }

    return render(request, "membership/change.html", context)
