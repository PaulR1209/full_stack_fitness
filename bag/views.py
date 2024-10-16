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
    grand_total = 0
    item_count = 0

    if membership_id:
        membership = get_object_or_404(Membership, id=membership_id)
        grand_total = (
            membership.price
        )
        item_count = 1

    return render(
        request,
        "bag/bag.html",
        {
            "membership": membership,
            "grand_total": grand_total,
            "item_count": item_count,
        },
    )


def remove_from_cart(request):
    request.session["cart_id"] = None
    request.session["cart_count"] = 0
    messages.success(request, "Membership removed from cart.")
    return redirect("membership")
