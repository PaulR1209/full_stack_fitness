from django.shortcuts import render, redirect, get_object_or_404
from membership.models import Membership
from django.contrib import messages


def add_to_cart(request, membership_id):
    membership = get_object_or_404(Membership, id=membership_id)

    if request.session.get("cart_count", 0) == 0:
        request.session["cart_id"] = membership.id
        request.session["cart_count"] = 1
        messages.success(
            request, f"Added {membership.membership_type} membership to your basket!"
        )

        return redirect("bag")
    else:
        messages.error(
            request,
            "You can only purchse one membership at a time. Please remove the current membership from your cart before adding another.",
        )

    return redirect("membership")


def cart_view(request):
    membership_id = request.session.get("cart_id")
    membership = None

    if membership_id:
        membership = get_object_or_404(Membership, id=membership_id)

    return render(request, "bag/bag.html", {"membership": membership})


def remove_from_cart(request):
    request.session["cart_id"] = None
    request.session["cart_count"] = 0
    messages.success(request, "Membership removed from cart.")
    return redirect("membership")
