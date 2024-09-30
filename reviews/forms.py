from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "title", "content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Write your review here..."}
            ),
            "rating": forms.Select(attrs={"class": "form-select"}),
        }
