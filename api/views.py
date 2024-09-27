import logging
from django.core.cache import cache
from rest_framework import generics
from .models import Item
from .serializers import ItemSerializer
from rest_framework.permissions import IsAuthenticated

# Initialize logger for the app
logger = logging.getLogger('__name__')

class ItemListCreateView(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Try to retrieve cached items first
        cached_items = cache.get('item_list')
        if cached_items:
            logger.info(f"Retrieved item list from cache for user {self.request.user}.")
            return cached_items
        
        # If no cache, retrieve from database
        logger.info(f"{self.request.user} requested the item list from database.")
        items = super().get_queryset()

        # Cache the result for future requests
        cache.set('item_list', items, timeout=60*15)  # Cache for 15 minutes
        return items

    def perform_create(self, serializer):
        # Save new item and log creation
        item = serializer.save()
        logger.info(f"New item created by {self.request.user}: {item}")

        # Invalidate cache since data has changed
        cache.delete('item_list')
        logger.info(f"Cache invalidated for item list after creation by {self.request.user}.")

class ItemDetailUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        # Log item retrieval and fetch from cache if available
        item_id = self.kwargs['pk']
        cached_item = cache.get(f'item_{item_id}')
        
        if cached_item:
            logger.info(f"Item {item_id} retrieved from cache by {self.request.user}.")
            return cached_item

        # If not cached, fetch from database
        response = super().retrieve(request, *args, **kwargs)
        logger.info(f"Item {item_id} retrieved by {self.request.user} from database.")

        # Cache the retrieved item
        cache.set(f'item_{item_id}', response.data, timeout=60*15)  # Cache for 15 minutes
        return response

    def update(self, request, *args, **kwargs):
        # Log item update
        item_id = self.kwargs['pk']
        response = super().update(request, *args, **kwargs)
        logger.info(f"Item {item_id} updated by {self.request.user}.")

        # Invalidate cache for both the item and item list
        cache.delete(f'item_{item_id}')
        cache.delete('item_list')
        logger.info(f"Cache invalidated for item {item_id} and item list after update by {self.request.user}.")
        return response

    def destroy(self, request, *args, **kwargs):
        # Log item deletion
        item_id = self.kwargs['pk']
        item = self.get_object()
        logger.info(f"Item {item_id} deleted by {self.request.user}.")
        
        response = super().destroy(request, *args, **kwargs)

        # Invalidate cache for both the item and item list
        cache.delete(f'item_{item_id}')
        cache.delete('item_list')
        logger.info(f"Cache invalidated for item {item_id} and item list after deletion by {self.request.user}.")
        return response
