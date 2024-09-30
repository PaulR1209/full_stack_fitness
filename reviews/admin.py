from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Review

class ReviewAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)
    list_display = ('user', 'rating', 'created_at')
    search_fields = ('content',)
    
admin.site.register(Review, ReviewAdmin)
