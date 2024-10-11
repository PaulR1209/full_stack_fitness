from django.db import models
from django.contrib.auth.models import User
from membership.models import Membership
import uuid
from dateutil.relativedelta import relativedelta

# Create your models here.


class Order(models.Model):
    order_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(null=True)
    phone_number = models.CharField(max_length=15 , null=True)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_renewed = models.DateTimeField(auto_now=True)
    next_renewal = models.DateTimeField()
    is_paid = models.BooleanField(default=False)
    cancellation_date = models.DateTimeField(null=True, blank=True)
    is_cancelled = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # If the order is being created for the first time, set the next_renewal date to 1 month from the created_at date
        if not self.pk:
            self.next_renewal = self.created_at + relativedelta(months=1)
        super().save(*args, **kwargs)

    def calculate_next_renewal(self):
        # Calculate the next renewal date by adding 1 month to the last_renewed date
        self.next_renewal = self.last_renewed + relativedelta(months=1)
        self.save()

    def __str__(self):
        return f"Order {self.order_number} - {self.membership.membership_type}"


class RecurringPayment(models.Model):
    PAYMENT_STATUS = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ]
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="recurring_payments"
    )
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    next_payment_date = models.DateTimeField()
    payment_status = models.CharField(
        max_length=10, choices=PAYMENT_STATUS, default="pending"
    )

    def save(self, *args, **kwargs):
        # If the payment is being created for the first time, set the next_payment_date to the calculated next renewal date
        if not self.pk:
            self.next_payment_date = self.order.calculate_next_renewal()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment for {self.order.membership.membership_type} - Due on {self.next_payment_date}"


class PaymentHistory(models.Model):
    PAYMENT_STATUS = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("failed", "Failed"),
    ]
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="payment_history"
    )
    amount = models.DecimalField(max_digits=6, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=10, choices=PAYMENT_STATUS, default="pending"
    )
    payment_method = models.CharField(max_length=50)
    transaction_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"Payment for {self.order.membership.membership_type} - {self.payment_status}"
