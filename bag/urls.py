from django.contrib import admin
from django.urls import path
from bag import views

urlpatterns = [
    path('', views.bag, name='bag'),
]