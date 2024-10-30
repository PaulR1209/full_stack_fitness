from django.shortcuts import render
from .models import Membership
from checkout.models import Order


def membership(request):
    memberships = Membership.objects.all()
    user_order = None
    if request.user.is_authenticated:
        user_order = Order.objects.filter(user=request.user).first()

    return render(request, 'membership/membership.html', {
        'memberships': memberships,
        'user_order': user_order
        })


def manage(request):
    user_order = None

    if request.user.is_authenticated:
        user_order = Order.objects.filter(user=request.user).first()

    return render(request, 'membership/manage.html' , {
        'user_order': user_order
        })
