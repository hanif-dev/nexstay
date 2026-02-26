from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from reservations.models import Reservation
import uuid
from decimal import Decimal

class Payment(models.Model):
    """Main payment record"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
        ('partially_refunded', 'Partially Refunded'),
        ('cancelled', 'Cancelled'),
    )
    
    METHOD_CHOICES = (
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('virtual_account', 'Virtual Account'),
        ('qris', 'QRIS'),
        ('ota_booking', 'OTA Platform'),
        ('gopay', 'GoPay'),
        ('ovo', 'OVO'),
        ('dana', 'DANA'),
        ('cash', 'Cash'),
    )

    reservation = models.ForeignKey(Reservation, on_delete=models.PROTECT, related_name='payments')
    transaction_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    
    # Amount breakdown
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, help_text="Room price x nights")
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="PPN 11%")
    service_charge = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Service 5-10%")
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Payment details
    currency = models.CharField(max_length=3, default='IDR')
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    
    # External payment gateway
    stripe_payment_intent = models.CharField(max_length=200, blank=True)
    stripe_charge_id = models.CharField(max_length=200, blank=True)
    midtrans_order_id = models.CharField(max_length=200, blank=True)
    xendit_invoice_id = models.CharField(max_length=200, blank=True)
    
    # Refund handling
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    refund_reason = models.TextField(blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    notes = models.TextField(blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['payment_method']),
        ]

    def __str__(self):
        return f"{self.transaction_id} - {self.status} ({self.currency} {self.total_amount:,.2f})"

    @property
    def is_paid(self):
        return self.status == 'completed'
    
    @property
    def is_refundable(self):
        return self.status == 'completed' and self.refund_amount < self.total_amount

    def calculate_totals(self):
        """Calculate tax, service charge, and total"""
        self.tax_amount = self.subtotal * Decimal('0.11')  # PPN 11%
        self.service_charge = self.subtotal * Decimal('0.05')  # Service 5%
        self.total_amount = self.subtotal + self.tax_amount + self.service_charge - self.discount_amount
        return self.total_amount


class OTASource(models.Model):
    """Channel Manager - OTA Platform Integration"""
    OTA_CHOICES = (
        ('direct', 'Direct Website'),
        ('booking_com', 'Booking.com'),
        ('expedia', 'Expedia'),
        ('agoda', 'Agoda'),
        ('traveloka', 'Traveloka'),
        ('tiket_com', 'Tiket.com'),
        ('pegi_pegi', 'PegiPegi'),
        ('airbnb', 'Airbnb'),
        ('trip_com', 'Trip.com'),
    )

    reservation = models.OneToOneField(Reservation, on_delete=models.CASCADE, related_name='ota_source')
    platform = models.CharField(max_length=20, choices=OTA_CHOICES, default='direct')
    ota_booking_id = models.CharField(max_length=100, blank=True, help_text="Booking ID dari platform")
    ota_commission_rate = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Commission rate in %, e.g., 15.00 for 15%"
    )
    ota_commission_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    gross_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Total booking amount")
    net_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="After commission")
    
    # Sync status
    is_synced = models.BooleanField(default=False)
    synced_at = models.DateTimeField(null=True, blank=True)
    sync_error = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'ota_sources'
        verbose_name = 'OTA Source'
        verbose_name_plural = 'OTA Sources'

    def __str__(self):
        return f"{self.get_platform_display()} - {self.ota_booking_id or 'No ID'}"
    
    def calculate_commission(self):
        """Calculate OTA commission and net revenue"""
        if self.gross_revenue > 0:
            self.ota_commission_amount = self.gross_revenue * (self.ota_commission_rate / 100)
            self.net_revenue = self.gross_revenue - self.ota_commission_amount
        return self.net_revenue


class DynamicPricing(models.Model):
    """Dynamic pricing based on season/demand - Hilton style"""
    SEASON_CHOICES = (
        ('low', 'Low Season'),
        ('mid', 'Mid Season'),
        ('high', 'High Season'),
        ('peak', 'Peak / Holiday'),
    )

    property_type = models.ForeignKey('properties.PropertyType', on_delete=models.CASCADE, related_name='dynamic_prices')
    season = models.CharField(max_length=10, choices=SEASON_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    
    # Pricing strategy
    price_multiplier = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        default=Decimal('1.00'),
        validators=[MinValueValidator(Decimal('0.50')), MaxValueValidator(Decimal('5.00'))],
        help_text="1.0 = base price, 1.5 = 50% increase, 0.8 = 20% discount"
    )
    min_price = models.DecimalField(max_digits=12, decimal_places=2)
    max_price = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Weekday/weekend differential
    weekend_multiplier = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('1.00'))
    
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0, help_text="Higher priority overrides lower")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dynamic_pricing'
        ordering = ['-priority', 'start_date']
        indexes = [
            models.Index(fields=['start_date', 'end_date', 'is_active']),
        ]

    def __str__(self):
        return f"{self.property_type.name} - {self.get_season_display()} ({self.start_date} to {self.end_date})"
    
    def calculate_price(self, base_price, is_weekend=False):
        """Calculate dynamic price based on multipliers"""
        price = base_price * self.price_multiplier
        if is_weekend:
            price *= self.weekend_multiplier
        
        # Enforce min/max bounds
        if price < self.min_price:
            return self.min_price
        elif price > self.max_price:
            return self.max_price
        return price


class DiscountCoupon(models.Model):
    """Promo codes and discount coupons"""
    DISCOUNT_TYPES = (
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount'),
        ('free_night', 'Free Night'),
    )

    code = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=200)
    discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPES)
    discount_value = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Usage limits
    max_uses = models.IntegerField(default=0, help_text="0 = unlimited")
    current_uses = models.IntegerField(default=0)
    max_uses_per_user = models.IntegerField(default=1)
    
    # Validity
    valid_from = models.DateField()
    valid_until = models.DateField()
    min_nights = models.IntegerField(default=1)
    min_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Restrictions
    property_types = models.ManyToManyField('properties.PropertyType', blank=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'discount_coupons'

    def __str__(self):
        return f"{self.code} - {self.discount_type}"
    
    @property
    def is_valid(self):
        from django.utils import timezone
        today = timezone.now().date()
        return (
            self.is_active and
            self.valid_from <= today <= self.valid_until and
            (self.max_uses == 0 or self.current_uses < self.max_uses)
        )


class LoyaltyProgram(models.Model):
    """HHonors-style loyalty program configuration"""
    TIER_CHOICES = (
        ('member', 'Member'),
        ('silver', 'Silver'),
        ('gold', 'Gold'),
        ('diamond', 'Diamond'),
    )

    tier = models.CharField(max_length=20, choices=TIER_CHOICES, unique=True)
    points_required = models.IntegerField(default=0)
    earn_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('1.00'),
                                    help_text="Points earned per IDR spent")
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    free_breakfast = models.BooleanField(default=False)
    free_upgrade = models.BooleanField(default=False)
    late_checkout = models.BooleanField(default=False)
    priority_support = models.BooleanField(default=False)
    
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'loyalty_programs'
        ordering = ['points_required']

    def __str__(self):
        return f"{self.get_tier_display()} - {self.points_required} pts"


class LoyaltyAccount(models.Model):
    """Guest loyalty account"""
    guest = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='loyalty')
    tier = models.CharField(max_length=20, choices=LoyaltyProgram.TIER_CHOICES, default='member')
    total_points = models.IntegerField(default=0)
    lifetime_points = models.IntegerField(default=0)
    tier_qualifying_nights = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'loyalty_accounts'

    def __str__(self):
        return f"{self.guest.email} - {self.tier} ({self.total_points} pts)"
    
    def add_points(self, points, description, reservation=None):
        """Add loyalty points"""
        self.total_points += points
        self.lifetime_points += points
        self.save()
        
        LoyaltyTransaction.objects.create(
            loyalty=self,
            reservation=reservation,
            points=points,
            description=description
        )
        
        # Check for tier upgrade
        self.check_tier_upgrade()
    
    def check_tier_upgrade(self):
        """Auto-upgrade tier based on lifetime points"""
        tiers = LoyaltyProgram.objects.filter(is_active=True).order_by('-points_required')
        for tier in tiers:
            if self.lifetime_points >= tier.points_required:
                if self.tier != tier.tier:
                    self.tier = tier.tier
                    self.save()
                break


class LoyaltyTransaction(models.Model):
    """Loyalty points transaction history"""
    loyalty = models.ForeignKey(LoyaltyAccount, on_delete=models.CASCADE, related_name='transactions')
    reservation = models.ForeignKey(Reservation, on_delete=models.SET_NULL, null=True, blank=True)
    points = models.IntegerField(help_text="Positive = earned, negative = redeemed")
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'loyalty_transactions'
        ordering = ['-created_at']

    def __str__(self):
        sign = '+' if self.points > 0 else ''
        return f"{self.loyalty.guest.email} {sign}{self.points} pts"


class CancellationPolicy(models.Model):
    """Cancellation policy with fee structure"""
    POLICY_TYPES = (
        ('flexible', 'Flexible'),
        ('moderate', 'Moderate'),
        ('strict', 'Strict'),
        ('non_refundable', 'Non-Refundable'),
    )

    property_type = models.ForeignKey('properties.PropertyType', on_delete=models.CASCADE, related_name='cancellation_policies')
    policy_type = models.CharField(max_length=20, choices=POLICY_TYPES)
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    # Refund structure
    days_before_checkin = models.IntegerField(help_text="Free cancellation if X days before check-in")
    refund_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=100,
                                            validators=[MinValueValidator(0), MaxValueValidator(100)])
    cancellation_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'cancellation_policies'
        verbose_name_plural = 'Cancellation Policies'

    def __str__(self):
        return f"{self.property_type.name} - {self.name}"
    
    def calculate_refund(self, total_amount, days_until_checkin):
        """Calculate refund amount based on policy"""
        if days_until_checkin >= self.days_before_checkin:
            # Full or partial refund
            refund = total_amount * (self.refund_percentage / 100)
            return refund - self.cancellation_fee
        else:
            # Late cancellation - no refund
            return Decimal('0.00')


class Invoice(models.Model):
    """Invoice/receipt for payment"""
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name='invoice')
    invoice_number = models.CharField(max_length=50, unique=True)
    issued_date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    
    # Billing details
    bill_to_name = models.CharField(max_length=200)
    bill_to_email = models.EmailField()
    bill_to_address = models.TextField(blank=True)
    
    notes = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to='invoices/', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'invoices'
        ordering = ['-created_at']

    def __str__(self):
        return f"Invoice {self.invoice_number}"
    
    def save(self, *args, **kwargs):
        if not self.invoice_number:
            from django.utils import timezone
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            self.invoice_number = f"INV-{timestamp}-{self.payment.transaction_id.hex[:8].upper()}"
        super().save(*args, **kwargs)
