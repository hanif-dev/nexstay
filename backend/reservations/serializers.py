from rest_framework import serializers
from .models import Reservation
from properties.serializers import PropertySerializer
from accounts.serializers import UserSerializer

class ReservationSerializer(serializers.ModelSerializer):
    guest = UserSerializer(read_only=True)
    unit = PropertySerializer(read_only=True)
    unit_id = serializers.IntegerField(write_only=True)
    nights = serializers.ReadOnlyField()

    class Meta:
        model = Reservation
        fields = ['id', 'guest', 'unit', 'unit_id', 'check_in', 'check_out', 
                  'num_guests', 'total_price', 'status', 'special_requests', 
                  'confirmation_code', 'nights', 'created_at']
        read_only_fields = ['confirmation_code', 'created_at']

    def validate(self, attrs):
        check_in = attrs.get('check_in')
        check_out = attrs.get('check_out')
        
        if check_in and check_out and check_in >= check_out:
            raise serializers.ValidationError("Check-out must be after check-in")
        
        return attrs


class ReservationCreateSerializer(serializers.ModelSerializer):
    unit_id = serializers.IntegerField()

    class Meta:
        model = Reservation
        fields = ['unit_id', 'check_in', 'check_out', 'num_guests', 'special_requests']

    def validate(self, attrs):
        check_in = attrs.get('check_in')
        check_out = attrs.get('check_out')
        
        if check_in >= check_out:
            raise serializers.ValidationError("Check-out must be after check-in")
        
        return attrs
