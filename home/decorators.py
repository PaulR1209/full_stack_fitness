from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from checkout.models import Order


def admin_required(view_func):
    """Decorator to check if the user is an admin."""

    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            messages.warning(
                request, "You need admin access to perform this action."
                )
            return redirect("index")
        return view_func(request, *args, **kwargs)

    return wrapper
