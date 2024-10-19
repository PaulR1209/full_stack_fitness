from django.shortcuts import render
from .models import Membership
from checkout.models import Order


def membership(request):
    user_order = None
    if request.user.is_authenticated:
        user_order = Order.objects.filter(user=request.user).first()

    membership_bronze = Membership.objects.filter(membership_type="Bronze").first()
    membership_silver = Membership.objects.filter(membership_type="Silver").first()
    membership_gold = Membership.objects.filter(membership_type="Gold").first()

    return render(
        request,
        "membership/membership.html",
        {
            "membership_bronze": membership_bronze,
            "membership_silver": membership_silver,
            "membership_gold": membership_gold,
            "user_order": user_order,
        },
    )


def manage(request):
    user_order = None
    recurring_payment = None
    payment_history = None

    if request.user.is_authenticated:
        user_order = Order.objects.filter(user=request.user).first()

        if user_order:
            # Get recurring payment and payment history related to the order
            recurring_payment = user_order.recurring_payments.first()
            payment_history = user_order.payment_history.all()

    membership_bronze = Membership.objects.filter(membership_type="Bronze").first()
    membership_silver = Membership.objects.filter(membership_type="Silver").first()
    membership_gold = Membership.objects.filter(membership_type="Gold").first()

    context = {
        "user_order": user_order,
        "recurring_payment": recurring_payment,
        "payment_history": payment_history,
        "membership_bronze": membership_bronze,
        "membership_silver": membership_silver,
        "membership_gold": membership_gold,
    }

    if user_order and user_order.is_cancelled:
        context["reactivate"] = True  # Control to show Reactivate button

    return render(request, "membership/manage.html", context)

