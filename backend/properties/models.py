from django.db import models
from django.core.validators import MinValueValidator
from slugify import slugify

class PropertyType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    max_guests = models.IntegerField(validators=[MinValueValidator(1)])
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    size_sqm = models.IntegerField()
    bed_configuration = models.CharField(max_length=200)
    view_type = models.CharField(max_length=100, blank=True)
    amenities = models.JSONField(default=list)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'property_types'
        ordering = ['base_price']
        verbose_name_plural = 'Property Types'
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Property(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Maintenance'),
        ('reserved', 'Reserved'),
    )
    
    property_type = models.ForeignKey(PropertyType, on_delete=models.PROTECT, related_name='properties')
    unit_number = models.CharField(max_length=20, unique=True)
    floor = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    notes = models.TextField(blank=True)
    last_maintenance = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'properties'
        ordering = ['floor', 'unit_number']
        verbose_name_plural = 'Properties'
        indexes = [models.Index(fields=['status', 'property_type'])]
    
    def __str__(self):
        return f"Unit {self.unit_number} - {self.property_type.name}"

class PropertyImage(models.Model):
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/')
    caption = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'property_images'
        ordering = ['order', '-is_primary']
    
    def __str__(self):
        return f"{self.property_type.name} - Image {self.order}"
