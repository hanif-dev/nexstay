from rest_framework import serializers
from .models import PropertyType, Property, PropertyImage

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'caption', 'is_primary', 'order']


class PropertyTypeSerializer(serializers.ModelSerializer):
    images = PropertyImageSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = PropertyType
        fields = ['id', 'name', 'slug', 'description', 'max_guests', 'base_price', 
                  'size_sqm', 'bed_configuration', 'view_type', 'amenities', 
                  'is_active', 'images', 'average_rating']

    def get_average_rating(self, obj):
        reviews = obj.reviews.filter(is_verified=True)
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return None


class PropertySerializer(serializers.ModelSerializer):
    property_type = PropertyTypeSerializer(read_only=True)

    class Meta:
        model = Property
        fields = ['id', 'property_type', 'unit_number', 'floor', 'status', 'notes']
