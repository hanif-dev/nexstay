from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import PropertyType, Property
from .serializers import PropertyTypeSerializer, PropertySerializer

class PropertyTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PropertyType.objects.filter(is_active=True).prefetch_related('images', 'reviews')
    serializer_class = PropertyTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['max_guests', 'view_type']
    search_fields = ['name', 'description']
    ordering_fields = ['base_price', 'size_sqm']
    lookup_field = 'slug'


class PropertyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Property.objects.select_related('property_type').filter(status='available')
    serializer_class = PropertySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['property_type', 'floor', 'status']
