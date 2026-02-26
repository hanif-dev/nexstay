from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Payment, LoyaltyAccount
from .serializers import PaymentSerializer, LoyaltyAccountSerializer

class PaymentViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Payment.objects.filter(reservation__guest=user).select_related('reservation')


class LoyaltyAccountViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LoyaltyAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LoyaltyAccount.objects.filter(guest=self.request.user)
