from rest_framework import serializers
from .models import Review
from accounts.serializers import UserSerializer

class ReviewSerializer(serializers.ModelSerializer):
    guest = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'guest', 'property_type', 'rating', 'title', 'comment', 
                  'is_verified', 'created_at']
        read_only_fields = ['is_verified', 'created_at']
