from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Payment, OTASource, DynamicPricing, DiscountCoupon,
    LoyaltyProgram, LoyaltyAccount, LoyaltyTransaction,
    CancellationPolicy, Invoice
)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['transaction_id_short', 'reservation_code', 'total_display', 'status_badge', 'payment_method', 'paid_at']
    list_filter = ['status', 'payment_method', 'currency', 'created_at']
    search_fields = ['transaction_id', 'reservation__confirmation_code', 'stripe_payment_intent']
    readonly_fields = ['transaction_id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('reservation', 'transaction_id', 'status', 'payment_method')
        }),
        ('Amount Breakdown', {
            'fields': ('subtotal', 'tax_amount', 'service_charge', 'discount_amount', 'total_amount', 'currency')
        }),
        ('Payment Gateway', {
            'fields': ('stripe_payment_intent', 'stripe_charge_id', 'midtrans_order_id', 'xendit_invoice_id')
        }),
        ('Refund', {
            'fields': ('refund_amount', 'refund_reason', 'refunded_at')
        }),
        ('Metadata', {
            'fields': ('notes', 'paid_at', 'created_at', 'updated_at')
        }),
    )
    
    def transaction_id_short(self, obj):
        return str(obj.transaction_id)[:13] + '...'
    transaction_id_short.short_description = 'Transaction ID'
    
    def reservation_code(self, obj):
        return obj.reservation.confirmation_code
    reservation_code.short_description = 'Booking Code'
    
    def total_display(self, obj):
        return f"{obj.currency} {obj.total_amount:,.2f}"
    total_display.short_description = 'Total'
    
    def status_badge(self, obj):
        colors = {
            'pending': 'orange',
            'processing': 'blue',
            'completed': 'green',
            'failed': 'red',
            'refunded': 'purple',
            'cancelled': 'gray',
        }
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'


@admin.register(OTASource)
class OTASourceAdmin(admin.ModelAdmin):
    list_display = ['reservation', 'platform_badge', 'ota_booking_id', 'commission_display', 'net_revenue_display', 'sync_status']
    list_filter = ['platform', 'is_synced']
    search_fields = ['ota_booking_id', 'reservation__confirmation_code']
    readonly_fields = ['created_at', 'updated_at']
    
    def platform_badge(self, obj):
        return format_html(
            '<strong>{}</strong>',
            obj.get_platform_display()
        )
    platform_badge.short_description = 'Platform'
    
    def commission_display(self, obj):
        return f"{obj.ota_commission_rate}% (IDR {obj.ota_commission_amount:,.2f})"
    commission_display.short_description = 'Commission'
    
    def net_revenue_display(self, obj):
        return f"IDR {obj.net_revenue:,.2f}"
    net_revenue_display.short_description = 'Net Revenue'
    
    def sync_status(self, obj):
        if obj.is_synced:
            return format_html('<span style="color: green;">✓ Synced</span>')
        return format_html('<span style="color: orange;">⚠ Not Synced</span>')
    sync_status.short_description = 'Sync'


@admin.register(DynamicPricing)
class DynamicPricingAdmin(admin.ModelAdmin):
    list_display = ['property_type', 'season_badge', 'date_range', 'multiplier_display', 'price_range', 'is_active']
    list_filter = ['season', 'is_active', 'property_type']
    date_hierarchy = 'start_date'
    
    def season_badge(self, obj):
        colors = {'low': 'green', 'mid': 'blue', 'high': 'orange', 'peak': 'red'}
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.season, 'gray'),
            obj.get_season_display()
        )
    season_badge.short_description = 'Season'
    
    def date_range(self, obj):
        return f"{obj.start_date} → {obj.end_date}"
    date_range.short_description = 'Period'
    
    def multiplier_display(self, obj):
        return f"{obj.price_multiplier}x"
    multiplier_display.short_description = 'Multiplier'
    
    def price_range(self, obj):
        return f"IDR {obj.min_price:,.0f} - {obj.max_price:,.0f}"
    price_range.short_description = 'Price Range'


@admin.register(DiscountCoupon)
class DiscountCouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_display', 'usage_display', 'validity', 'is_active']
    list_filter = ['discount_type', 'is_active', 'valid_from', 'valid_until']
    search_fields = ['code', 'description']
    filter_horizontal = ['property_types']
    
    def discount_display(self, obj):
        if obj.discount_type == 'percentage':
            return f"{obj.discount_value}%"
        elif obj.discount_type == 'fixed':
            return f"IDR {obj.discount_value:,.0f}"
        return "Free Night"
    discount_display.short_description = 'Discount'
    
    def usage_display(self, obj):
        if obj.max_uses == 0:
            return f"{obj.current_uses} / ∞"
        return f"{obj.current_uses} / {obj.max_uses}"
    usage_display.short_description = 'Used'
    
    def validity(self, obj):
        return f"{obj.valid_from} → {obj.valid_until}"
    validity.short_description = 'Valid Period'


@admin.register(LoyaltyProgram)
class LoyaltyProgramAdmin(admin.ModelAdmin):
    list_display = ['tier_badge', 'points_required', 'earn_rate', 'benefits', 'is_active']
    list_filter = ['is_active']
    
    def tier_badge(self, obj):
        colors = {'member': 'gray', 'silver': 'silver', 'gold': 'gold', 'diamond': 'cyan'}
        return format_html(
            '<span style="background: {}; color: white; padding: 5px 15px; border-radius: 3px; font-weight: bold;">{}</span>',
            colors.get(obj.tier, 'gray'),
            obj.get_tier_display().upper()
        )
    tier_badge.short_description = 'Tier'
    
    def benefits(self, obj):
        perks = []
        if obj.discount_percentage > 0:
            perks.append(f"{obj.discount_percentage}% off")
        if obj.free_breakfast:
            perks.append("Breakfast")
        if obj.free_upgrade:
            perks.append("Upgrade")
        if obj.late_checkout:
            perks.append("Late checkout")
        return ", ".join(perks) or "None"
    benefits.short_description = 'Benefits'


@admin.register(LoyaltyAccount)
class LoyaltyAccountAdmin(admin.ModelAdmin):
    list_display = ['guest', 'tier_badge', 'points_display', 'nights', 'updated_at']
    list_filter = ['tier']
    search_fields = ['guest__email', 'guest__first_name', 'guest__last_name']
    readonly_fields = ['created_at', 'updated_at']
    
    def tier_badge(self, obj):
        colors = {'member': 'gray', 'silver': 'silver', 'gold': 'gold', 'diamond': 'cyan'}
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.tier, 'gray'),
            obj.get_tier_display()
        )
    tier_badge.short_description = 'Tier'
    
    def points_display(self, obj):
        return f"{obj.total_points:,} ({obj.lifetime_points:,} lifetime)"
    points_display.short_description = 'Points'
    
    def nights(self, obj):
        return obj.tier_qualifying_nights
    nights.short_description = 'Nights'


@admin.register(LoyaltyTransaction)
class LoyaltyTransactionAdmin(admin.ModelAdmin):
    list_display = ['guest_email', 'points_display', 'description', 'reservation_code', 'created_at']
    list_filter = ['created_at']
    search_fields = ['loyalty__guest__email', 'description']
    date_hierarchy = 'created_at'
    
    def guest_email(self, obj):
        return obj.loyalty.guest.email
    guest_email.short_description = 'Guest'
    
    def points_display(self, obj):
        color = 'green' if obj.points > 0 else 'red'
        sign = '+' if obj.points > 0 else ''
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}{}</span>',
            color, sign, obj.points
        )
    points_display.short_description = 'Points'
    
    def reservation_code(self, obj):
        return obj.reservation.confirmation_code if obj.reservation else '-'
    reservation_code.short_description = 'Booking'


@admin.register(CancellationPolicy)
class CancellationPolicyAdmin(admin.ModelAdmin):
    list_display = ['property_type', 'policy_badge', 'refund_terms', 'is_default', 'is_active']
    list_filter = ['policy_type', 'is_active', 'is_default']
    
    def policy_badge(self, obj):
        colors = {'flexible': 'green', 'moderate': 'orange', 'strict': 'red', 'non_refundable': 'darkred'}
        return format_html(
            '<span style="background: {}; color: white; padding: 3px 10px; border-radius: 3px;">{}</span>',
            colors.get(obj.policy_type, 'gray'),
            obj.get_policy_type_display()
        )
    policy_badge.short_description = 'Policy'
    
    def refund_terms(self, obj):
        return f"{obj.refund_percentage}% if {obj.days_before_checkin}+ days before"
    refund_terms.short_description = 'Terms'


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'payment_txn', 'bill_to_name', 'issued_date', 'pdf_link']
    search_fields = ['invoice_number', 'bill_to_email', 'payment__transaction_id']
    readonly_fields = ['invoice_number', 'created_at']
    date_hierarchy = 'issued_date'
    
    def payment_txn(self, obj):
        return str(obj.payment.transaction_id)[:13] + '...'
    payment_txn.short_description = 'Payment'
    
    def pdf_link(self, obj):
        if obj.pdf_file:
            return format_html('<a href="{}" target="_blank">Download PDF</a>', obj.pdf_file.url)
        return '-'
    pdf_link.short_description = 'PDF'
