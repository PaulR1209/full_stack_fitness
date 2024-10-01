from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def review_list(request):
    selected_rating = request.GET.get("rating")

    reviews = Review.objects.all()

    if selected_rating:
        reviews = reviews.filter(rating=selected_rating)

    for review in reviews:
        review.filled_stars = range(review.rating)
        review.empty_stars = range(5 - review.rating)

    return render(
        request,
        "reviews/reviews.html",
        {
            "reviews": reviews,
            "selected_rating": selected_rating,
            "rating_range": range(1, 6),
        },
    )


@login_required
def review_create(request):
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, "Thank you for your review!")
            return redirect("reviews")
    else:
        form = ReviewForm()
    return render(request, "reviews/review_form.html", {"form": form})


@login_required
def review_edit(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if review.user != request.user:
        messages.error(request, "You don't have permission to edit this review.")
        return redirect("reviews")

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Review updated successfully.")
            return redirect("reviews")
    else:
        form = ReviewForm(instance=review)
    return render(request, "reviews/review_form.html", {"form": form})


@login_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)

    if review.user != request.user:
        messages.error(request, "You don't have permission to delete this review.")
        return redirect("reviews")

    if request.method == "POST":
        review.delete()
        messages.success(request, "Review deleted successfully.")
        return redirect("reviews")
    return render(request, "reviews/review_delete.html", {"review": review})
