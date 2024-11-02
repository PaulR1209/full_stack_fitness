from django.db import models
from django.contrib.auth.models import User
import uuid


class Invoice(models.Model):
    """Model to store invoice information."""
    invoice_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    order = models.ForeignKey('checkout.Order', on_delete=models.CASCADE, related_name='invoices')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice {self.invoice_number} - Order {self.order.order_number}"