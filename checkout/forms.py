from django import forms
from membership.models import Order


class OrderForm(forms.Form):
    class Meta:
        model = Order
        fields = ["email", "phone_number"]
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email"}),
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone Number"}),
        }