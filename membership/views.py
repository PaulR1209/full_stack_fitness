from django.shortcuts import render
from .models import Membership

# Create your views here.


def membership(request):
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
        },
    )
