from django.db import models
from django.contrib.auth.models import User
from membership.models import Membership
import uuid
from dateutil.relativedelta import relativedelta


class Order(models.Model):
    """Model to store order information."""
    order_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, default="")
    email = models.EmailField(null=True, blank=True)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    pending_membership = models.ForeignKey(
        Membership,
        on_delete=models.CASCADE,
        related_name="pending_membership",
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    last_renewed = models.DateTimeField(null=True, blank=True)
    next_renewal = models.DateTimeField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    cancellation_date = models.DateTimeField(null=True, blank=True)
    is_cancelled = models.BooleanField(default=False)
    subscription_id = models.CharField(max_length=100, null=True, blank=True)
    stripe_price_id = models.CharField(max_length=100, null=True, blank=True)

    def calculate_next_renewal(self):
        """Calculate the next renewal date."""
        if self.last_renewed:
            self.next_renewal = self.last_renewed + relativedelta(months=1)

    def __str__(self):
        return f"Order {self.order_number} - {self.membership.membership_type}"
