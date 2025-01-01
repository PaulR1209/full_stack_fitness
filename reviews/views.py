from django.shortcuts import render, redirect, get_object_or_404
from .models import Review
from .forms import ReviewForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def review_list(request):
    """Display all reviews with optional filtering and sorting."""

    # Get the selected rating from the query parameters
    selected_rating = request.GET.get("rating")
    # Get the sorting option from the query parameters, defaulting to "newest"
    sorted_by = request.GET.get("sort", "newest")

    # Retrieve all reviews from the database
    reviews = Review.objects.all()

    # Filter reviews by selected rating if provided
    if selected_rating:
        reviews = reviews.filter(rating=selected_rating)

    # Sort reviews based on the selected option
    if sorted_by == "newest":
        reviews = reviews.order_by("-created_at")
    elif sorted_by == "oldest":
        reviews = reviews.order_by("created_at")
    elif sorted_by == "lowest":
        reviews = reviews.order_by("rating")
    elif sorted_by == "highest":
        reviews = reviews.order_by("-rating")

    # Calculate the filled and empty stars for displaying the rating
    for review in reviews:
        review.filled_stars = range(review.rating)
        review.empty_stars = range(5 - review.rating)

    # Render the reviews page with the filtered and sorted reviews
    return render(
        request,
        "reviews/reviews.html",
        {
            "reviews": reviews,
            "selected_rating": selected_rating,
            "sorted_by": sorted_by,
            "rating_range": range(1, 6),
        },
    )


@login_required
def review_create(request):
    """Create a new review."""
    if request.method == "POST":
        # Create a ReviewForm with the posted data
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, "Thank you for your review!")
            return redirect("reviews")
    else:
        form = ReviewForm()  # Create an empty form
    return render(request, "reviews/review_form.html", {"form": form})


@login_required
def review_edit(request, pk):
    """Edit an existing review."""
    # Retrieve the review by primary key or return a 404 if not found
    review = get_object_or_404(Review, pk=pk)

    # Check if the logged-in user is the owner of the review
    if review.user != request.user and not request.user.is_staff:
        messages.error(
            request, "You don't have permission to edit this review."
            )
        return redirect("reviews")

    if request.method == "POST":
        # Create a ReviewForm with the posted data and the existing review
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Review updated successfully.")
            return redirect("reviews")
    else:
        form = ReviewForm(
            instance=review
        )  # Create a form with the existing review instance
    return render(request, "reviews/review_form.html", {"form": form})


@login_required
def review_delete(request, pk):
    """Delete an existing review."""
    # Retrieve the review by primary key or return a 404 if not found
    review = get_object_or_404(Review, pk=pk)

    # Check if the logged-in user is the owner of the review
    if review.user != request.user and not request.user.is_staff:
        messages.error(
            request, "You don't have permission to delete this review."
            )
        return redirect("reviews")

    # Display a confirmation page for deleting the review
    if request.method == "POST":
        review.delete()
        messages.success(request, "Review deleted successfully.")
        return redirect("reviews")
    return render(request, "reviews/review_delete.html", {"review": review})
