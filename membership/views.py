from django.shortcuts import render
from .models import Membership

# Create your views here.


def membership(request):
    membership_bronze = Membership.objects.get(membership_type="Bronze")
    membership_silver = Membership.objects.get(membership_type="Silver")
    membership_gold = Membership.objects.get(membership_type="Gold")

    return render(
        request,
        "membership/membership.html",
        {
            "membership_bronze": membership_bronze,
            "membership_silver": membership_silver,
            "membership_gold": membership_gold,
        },
    )
