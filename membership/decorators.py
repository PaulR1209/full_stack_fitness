from django.shortcuts import redirect
from django.contrib import messages
from checkout.models import Order

def membership_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not Order.objects.filter(user=request.user, is_expired=False).exists():
            messages.warning(request, "You need an active membership to access this page.")
            return redirect("membership")
        return view_func(request, *args, **kwargs)
    return wrapper