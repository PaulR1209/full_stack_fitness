from django import forms
from .models import Review
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit



class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "title", "content"]
        labels = {
            "title": "Title",
            "content": "Write your review here"
        }
