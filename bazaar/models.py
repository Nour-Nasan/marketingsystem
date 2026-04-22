from django.conf import settings
from django.db import models


BOOKING_STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
    ('cancelled', 'Cancelled'),
]


class Bazaar(models.Model):
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='organized_bazaars',
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    main_image = models.ImageField(upload_to='bazaar_images/')
    location = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    table_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BazaarBooking(models.Model):
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bazaar_bookings',
    )
    bazaar = models.ForeignKey(
        Bazaar,
        on_delete=models.CASCADE,
        related_name='bookings',
    )
    status = models.CharField(
        max_length=20,
        choices=BOOKING_STATUS_CHOICES,
        default='pending',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['seller', 'bazaar'],
                name='bazaar_booking_unique_seller_per_bazaar',
            ),
        ]

    def __str__(self):
        return f'Booking #{self.pk} — {self.seller} → {self.bazaar}'
