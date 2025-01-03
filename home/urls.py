from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("admin_dashboard", views.admin_dashboard, name="admin_dashboard"),
]
