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
    ordering = ("-created_at",)
    search_fields = ("full_name", "email", "order_number")


admin.site.register(Order, OrderAdmin)
