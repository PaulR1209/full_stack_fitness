from django.shortcuts import render
from .forms import NewsletterSignupForm
from django.contrib import messages

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
