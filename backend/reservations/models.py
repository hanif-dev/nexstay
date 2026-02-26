from django.db import models
from django.conf import settings
from properties.models import Property

class Reservation(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
    )
    
    guest = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='reservations')
    unit = models.ForeignKey(Property, on_delete=models.PROTECT, related_name='reservations')
    check_in = models.DateField()
    check_out = models.DateField()
    num_guests = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True)
    confirmation_code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'reservations'
        ordering = ['-check_in']
        indexes = [
            models.Index(fields=['check_in', 'check_out']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.confirmation_code} - {self.guest.email}"
    
    @property
    def nights(self):
        return (self.check_out - self.check_in).days
    
    def save(self, *args, **kwargs):
        if not self.confirmation_code:
            import uuid
            self.confirmation_code = str(uuid.uuid4()).upper()[:12]
        super().save(*args, **kwargs)
