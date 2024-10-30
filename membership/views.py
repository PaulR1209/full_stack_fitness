from django.shortcuts import render
from .models import Membership


def membership(request):
    memberships = Membership.objects.all()
    return render(request, 'membership/membership.html', {'memberships': memberships})
