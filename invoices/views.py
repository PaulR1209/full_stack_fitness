from django.shortcuts import render

# Create your views here.

def invoices(request):
    return render(request, 'invoices/invoices.html')