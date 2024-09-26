# inventory/views.py
from django.core.cache import cache
from rest_framework import generics
from rest_framework.response import Response
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
        cache_key = 'item_list'  # Key to cache the item list
        item_list = cache.get(cache_key)

        if item_list:
        # If item list is found in the cache, return it
            return item_list

        # If not found, fetch from the database and cache the result
        queryset = Item.objects.all()
        cache.set(cache_key, queryset, timeout=60*5)  # Cache for 5 minutes
        return queryset

    def perform_create(self, serializer):
        serializer.save()

        # Invalidate cache after a new item is created
        cache_key = 'item_list'
        cache.delete(cache_key)






# Retrieve, Update, and Delete an Item (GET, PUT, DELETE)
class ItemDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    
    def retrieve(self, request, *args, **kwargs):
        item_id = kwargs.get('pk')
        cache_key = f'item_{item_id}'
        
        # Try to fetch the item from Redis
        item_data = cache.get(cache_key)
        if item_data:
            return Response(item_data)

        # Fetch from the database
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        
        # Cache the serialized data for future requests
        cache.set(cache_key, serializer.data, timeout=60*5)  # Cache for 5 minutes
        
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        # Invalidate cache after update
        item_id = kwargs.get('pk')
        cache_key = f'item_{item_id}'
        cache.delete(cache_key)
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        # Invalidate cache after deletion
        item_id = kwargs.get('pk')
        cache_key = f'item_{item_id}'
        cache.delete(cache_key)
        return response