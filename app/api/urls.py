from django.urls import path
from . import views

urlpatterns = [
    path('products/', views.handleData, name='products'),
    path('purchases/', views.handlePurchase, name='purchases'),
]