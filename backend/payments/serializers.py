from rest_framework import serializers
from .models import Payment, OTASource, DiscountCoupon, LoyaltyAccount, Invoice

class PaymentSerializer(serializers.ModelSerializer):
    is_paid = serializers.ReadOnlyField()
    is_refundable = serializers.ReadOnlyField()

    class Meta:
        model = Payment
        fields = ['id', 'transaction_id', 'subtotal', 'tax_amount', 'service_charge', 
                  'discount_amount', 'total_amount', 'currency', 'status', 
                  'payment_method', 'is_paid', 'is_refundable', 'paid_at', 'created_at']
        read_only_fields = ['transaction_id', 'created_at']


class OTASourceSerializer(serializers.ModelSerializer):
    platform_display = serializers.CharField(source='get_platform_display', read_only=True)

    class Meta:
        model = OTASource
        fields = ['id', 'platform', 'platform_display', 'ota_booking_id', 
                  'ota_commission_rate', 'net_revenue', 'is_synced']


class DiscountCouponSerializer(serializers.ModelSerializer):
    is_valid = serializers.ReadOnlyField()

    class Meta:
        model = DiscountCoupon
        fields = ['code', 'description', 'discount_type', 'discount_value', 
                  'valid_from', 'valid_until', 'is_valid']


class LoyaltyAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoyaltyAccount
        fields = ['tier', 'total_points', 'lifetime_points', 'tier_qualifying_nights']


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = ['invoice_number', 'issued_date', 'bill_to_name', 'pdf_file']
