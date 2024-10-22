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

    if request.user.is_authenticated:
        user_order = (
            Order.objects.filter(user=request.user).order_by("-created_at").first()
        )

    membership_bronze = Membership.objects.filter(membership_type="Bronze").first()
    membership_silver = Membership.objects.filter(membership_type="Silver").first()
    membership_gold = Membership.objects.filter(membership_type="Gold").first()

    context = {
        "user_order": user_order,
        "membership_bronze": membership_bronze,
        "membership_silver": membership_silver,
        "membership_gold": membership_gold,
    }

    return render(request, "membership/manage.html", context)


def change(request):
    user_order = None

    if request.user.is_authenticated:
        user_order = (
            Order.objects.filter(user=request.user).order_by("-created_at").first()
        )

    membership_bronze = Membership.objects.filter(membership_type="Bronze").first()
    membership_silver = Membership.objects.filter(membership_type="Silver").first()
    membership_gold = Membership.objects.filter(membership_type="Gold").first()

    context = {
        "user_order": user_order,
        "membership_bronze": membership_bronze,
        "membership_silver": membership_silver,
        "membership_gold": membership_gold,
    }

    return render(request, "membership/change.html", context)