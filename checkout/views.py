from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import OrderForm

# Create your views here.


@login_required
def checkout(request):
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            return redirect("membership")
    else:
        form = OrderForm()
    return render(request, "checkout/checkout.html", {"form": form})
    