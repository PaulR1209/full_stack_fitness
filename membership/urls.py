from . import views
from django.urls import path

urlpatterns = [
    path('', views.membership, name='membership'),
    path('manage/', views.manage, name='manage'),
    path('change/', views.change, name='change')
]