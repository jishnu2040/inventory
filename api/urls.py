# inventory/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ItemListCreateView.as_view(), name='item-list-create'),  # List and Create
    path('<int:pk>/', views.ItemDetailUpdateDeleteView.as_view(), name='item-detail'),  # Retrieve, Update, Delete
]
