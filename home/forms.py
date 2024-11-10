from django import forms
from .models import NewsletterSignup
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class NewsletterSignupForm(forms.ModelForm):
    class Meta:
        model = NewsletterSignup
        fields = ["name", "email"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"placeholder": "Your email"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "POST"
        self.helper.add_input(Submit("submit", "Sign up"))

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if NewsletterSignup.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "This email is already signed up for the newsletter."
            )
        return email
