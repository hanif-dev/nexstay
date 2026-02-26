from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from decimal import Decimal
from datetime import date

from .models import Reservation
from .serializers import ReservationSerializer, ReservationCreateSerializer
from properties.models import Property


class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'admin':
            return Reservation.objects.all().select_related('guest', 'unit__property_type')
        return Reservation.objects.filter(guest=user).select_related('unit__property_type')

    def get_serializer_class(self):
        if self.action == 'create':
            return ReservationCreateSerializer
        return ReservationSerializer

    def perform_create(self, serializer):
        unit_id = self.request.data.get('unit_id')
        check_in = self.request.data.get('check_in')
        check_out = self.request.data.get('check_out')

        total_price = Decimal('0')

        try:
            unit = Property.objects.get(id=unit_id)
            ci = date.fromisoformat(str(check_in))
            co = date.fromisoformat(str(check_out))
            nights = (co - ci).days
            if nights > 0:
                base = Decimal(str(unit.property_type.base_price))
                tax = base * Decimal('0.11')
                service = base * Decimal('0.05')
                total_price = (base + tax + service) * nights
        except Exception as e:
            print(f"Price calculation error: {e}")

        serializer.save(guest=self.request.user, total_price=total_price)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        if reservation.status not in ['pending', 'confirmed']:
            return Response(
                {'error': 'Cannot cancel this reservation'},
                status=status.HTTP_400_BAD_REQUEST
            )
        reservation.status = 'cancelled'
        reservation.save()
        return Response({'status': 'Reservation cancelled'})
