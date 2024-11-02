from django.shortcuts import render
from checkout.views import sync_with_stripe

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        sync_with_stripe(request.user)
    return render(request, 'home/index.html')


def about(request):
    return render(request, 'home/about.html')