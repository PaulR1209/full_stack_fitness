# urls.py
from django.urls import path
from .views import review_list, review_create, review_edit, review_delete

urlpatterns = [
    path("", review_list, name="reviews"),
    path("new/", review_create, name="review_create"),
    path("edit/<int:pk>/", review_edit, name="review_edit"),
    path("delete/<int:pk>/", review_delete, name="review_delete"),
]
