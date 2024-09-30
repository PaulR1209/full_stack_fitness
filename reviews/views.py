# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from .forms import ReviewForm


def review_list(request):
    reviews = Review.objects.all()
    return render(request, "reviews/reviews.html", {"reviews": reviews})


def review_create(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect("reviews")
    else:
        form = ReviewForm()
    return render(request, "reviews/review_form.html", {"form": form})


def review_edit(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect("reviews")
    else:
        form = ReviewForm(instance=review)
    return render(request, "reviews/review_form.html", {"form": form})


def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == "POST":
        review.delete()
        return redirect("reviews")
    return render(request, "reviews/review_delete.html", {"review": review})
