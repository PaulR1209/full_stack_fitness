from django.shortcuts import render
from .forms import NewsletterSignupForm
from django.contrib import messages
from django.contrib.auth.models import User
from checkout.models import Order
from .decorators import admin_required

# Create your views here.


def index(request):
    if request.method == "POST":
        form = NewsletterSignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thank you for signing up!")
        else:
            messages.error(
                request, "This email is already signed up for the newsletter."
            )
    else:
        form = NewsletterSignupForm()

    return render(request, "home/index.html", {"form": form})


def about(request):
    return render(request, "home/about.html")


@admin_required
def admin_dashboard(request):

    all_users = User.objects.all()

    for user in all_users:
        user.orders = Order.objects.filter(user=user)

    return render(
        request,
        "home/admin_dashboard.html",
        {"all_users": all_users},
    )
