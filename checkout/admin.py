from django.contrib import admin
from .models import Order

class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "membership",
        "next_renewal",
        "is_paid",
        "is_cancelled",
    )
    readonly_fields = (
        "user",
        "membership",
        "full_name",
        "email",
        "created_at",
        "last_renewed",
        "next_renewal",
        "is_paid",
        "cancellation_date",
        "is_cancelled",
        "subscription_id",
        "order_number",
        "stripe_price_id",
    )
    ordering = ("-created_at",)
    search_fields = ("full_name", "email", "order_number")

admin.site.register(Order, OrderAdmin)