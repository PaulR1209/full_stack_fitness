from django.urls import path
from .views import Checkout, CheckoutSuccess, CheckoutError, CancelMembership, ReactivateMembership

urlpatterns = [
    path("",Checkout.as_view(),name="checkout",),
    path("success/", CheckoutSuccess.as_view(), name="success",),
    path("error/", CheckoutError.as_view(), name="error",),
    path("cancel-membership/", CancelMembership.as_view(), name="cancel_membership",),
    path("reactivate-membership/", ReactivateMembership.as_view(), name="reactivate_membership",),
]
