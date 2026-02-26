from django.contrib import admin
from .models import PropertyType, Property, PropertyImage

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1

@admin.register(PropertyType)
class PropertyTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'max_guests', 'base_price', 'size_sqm', 'is_active']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [PropertyImageInline]

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['unit_number', 'property_type', 'floor', 'status', 'last_maintenance']
    list_filter = ['status', 'property_type', 'floor']
    search_fields = ['unit_number', 'notes']
