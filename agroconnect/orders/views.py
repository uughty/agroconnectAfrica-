from django.shortcuts import render

def order_list(request):
    return render(request, 'orders/order_list.html')

# orders/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.order_list, name='order_list'),
]