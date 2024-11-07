from django.shortcuts import render
from .models import Membership
from checkout.models import Order
from checkout.views import check_and_update_payment_status
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .decorators import membership_required


def membership(request):
    """View to display the membership page."""
    memberships = Membership.objects.all()
    user_order = None
    if request.user.is_authenticated:
        user_order = Order.objects.filter(user=request.user).first()

    return render(
        request,
        "membership/membership.html",
        {"memberships": memberships, "user_order": user_order},
    )


@login_required
@membership_required
def manage(request):
    """View to display the manage membership page."""
    user_order = None
    subscription_id = None
    user = User.objects.filter(username=request.user).first()

    if request.user.is_authenticated:
        user_order = Order.objects.filter(user=request.user).first()
        if user_order:
            subscription_id = user_order.subscription_id

            check_and_update_payment_status(request, user, subscription_id)

    return render(
        request, "membership/manage.html", {"user_order": user_order}
        )


@login_required
@membership_required
def change(request):
    """View to display the change membership page."""
    user_order = None

    if request.user.is_authenticated:
        user_order = Order.objects.filter(user=request.user).first()

    return render(
        request, "membership/change.html", {"user_order": user_order}
        )
