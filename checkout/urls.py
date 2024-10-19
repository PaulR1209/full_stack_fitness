from django.urls import path
from .views import CheckoutView, SuccessView, CancelMembershipView, CancelConfirmationView, ReactivateMembershipView

urlpatterns = [
    path('', CheckoutView.as_view(), name='checkout'),
    path('success/', SuccessView.as_view(), name='success'),
    path('cancel/', CancelConfirmationView.as_view(), name='cancel'),
    path('confirm_cancel/', CancelMembershipView.as_view(), name='confirm_cancel'),
    path('reactivate/', ReactivateMembershipView.as_view(), name='reactivate'),
]
