from django.contrib import admin
from .models import NewsletterSignup

# Register your models here.


class NewsletterSignupAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "signup_date")
    search_fields = ("name", "email")
    list_filter = ("signup_date",)

admin.site.register(NewsletterSignup, NewsletterSignupAdmin)