from django.contrib import admin
from .models import Order, RecurringPayment, PaymentHistory

# Register your models here.

admin.site.register(Order)

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "user",
        "membership",
        "created_at",
        "last_renewed",
        "next_renewal",
        "is_paid",
        "cancellation_date",
        "is_cancelled",
    )

    readonly_fields = ("order_number", "created_at", "last_renewed", "next_renewal")

    ordering = ("-created_at",)

admin.site.register(RecurringPayment)

class RecurringPaymentAdmin(admin.ModelAdmin):
    list_display = ("order", "amount", "next_payment_date", "payment_status")

    readonly_fields = ("next_payment_date",)

    ordering = ("-next_payment_date",)

admin.site.register(PaymentHistory)

class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ("order", "amount", "payment_date", "payment_status")

    ordering = ("-payment_date",)