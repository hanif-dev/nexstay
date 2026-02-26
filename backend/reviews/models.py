from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from properties.models import PropertyType

class Review(models.Model):
    guest = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    property_type = models.ForeignKey(PropertyType, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200)
    comment = models.TextField()
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reviews'
        ordering = ['-created_at']
        unique_together = ['guest', 'property_type']
    
    def __str__(self):
        return f"{self.guest.email} - {self.property_type.name} ({self.rating}★)"
