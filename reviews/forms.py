from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["user", "rating", "content"]
        labels = {
            "user": "Username",
            "rating": "Rate your experience",
            "content": "Write your review",
        }
