from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['confirmation_code', 'guest', 'unit', 'check_in', 'check_out', 'status', 'total_price']
    list_filter = ['status', 'check_in', 'check_out']
    search_fields = ['confirmation_code', 'guest__email', 'unit__unit_number']
    readonly_fields = ['confirmation_code', 'created_at', 'updated_at']
