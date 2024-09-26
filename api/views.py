# inventory/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Item
from .serializers import ItemSerializer
import logging

# Configure logging
logger = logging.getLogger(__name__)

# List and Create Items (GET and POST)
class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Item.objects.all()  # Modify this if you want to filter by user or other criteria

    def perform_create(self, serializer):
        serializer.save()  # You may customize this if you want to save additional fields

# Retrieve, Update, and Delete an Item (GET, PUT, DELETE)
class ItemDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def get_queryset(self):
        logger.info(f"ItemDetailUpdateDeleteView called for user {self.request.user}")
        return Item.objects.all()  # Modify this if you want to filter by user or other criteria
