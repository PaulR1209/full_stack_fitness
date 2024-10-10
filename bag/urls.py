from django.urls import path
from .views import add_to_cart, cart_view, remove_from_cart

urlpatterns = [
    path("", cart_view, name="bag"),
    path("add_to_cart/<int:membership_id>/", add_to_cart, name="add_to_cart"),
    path("remove_from_cart/", remove_from_cart, name="remove_from_cart")
]
