from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """Form for creating a review"""
    class Meta:
        model = Review
        fields = ["rating", "content"]
        labels = {
            "rating": "Rate your experience",
            "content": "Write your review",
        }
