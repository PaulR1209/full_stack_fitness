from django.shortcuts import redirect
from django.contrib import messages
from checkout.models import Order


def membership_required(view_func):
    """Decorator to check if the user has an active membership."""
    def wrapper(request, *args, **kwargs):
        has_active_membership = Order.objects.filter(
            user=request.user, is_expired=False
        ).exists()

        if not request.user.is_authenticated or not has_active_membership:
            messages.warning(
                request, "You need an active membership to access this page."
            )
            return redirect("membership")
        return view_func(request, *args, **kwargs)

    return wrapper
