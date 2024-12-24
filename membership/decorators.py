from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
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


def admin_required(view_func):
    """Decorator to check if the user is an admin."""

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            messages.warning(request, "You need admin access to perform this action.")
            return redirect("home")
        return view_func(request, *args, **kwargs)

    return wrapper
