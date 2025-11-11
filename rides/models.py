from django.db import models
from django.utils import timezone


class User(models.Model):
    """
    Custom User model for riders and drivers.
    The assessment requires a custom User model with role field.
    """
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('rider', 'Rider'),
        ('driver', 'Driver'),
    ]

    id_user = models.AutoField(primary_key=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)

    class Meta:
        db_table = 'user'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['role']),
        ]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"


class Ride(models.Model):
    """
    Ride model representing a ride request.
    """
    STATUS_CHOICES = [
        ('en-route', 'En Route'),
        ('pickup', 'Pickup'),
        ('dropoff', 'Dropoff'),
    ]

    id_ride = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    id_rider = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rides_as_rider',
        db_column='id_rider'
    )
    id_driver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rides_as_driver',
        db_column='id_driver'
    )
    pickup_latitude = models.FloatField()
    pickup_longitude = models.FloatField()
    dropoff_latitude = models.FloatField()
    dropoff_longitude = models.FloatField()
    pickup_time = models.DateTimeField()

    class Meta:
        db_table = 'ride'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['pickup_time']),
            models.Index(fields=['id_rider']),
            models.Index(fields=['id_driver']),
            # For GPS-based distance sorting
            models.Index(fields=['pickup_latitude', 'pickup_longitude']),
        ]
        ordering = ['-pickup_time']

    def __str__(self):
        return f"Ride {self.id_ride} - {self.status}"


class RideEvent(models.Model):
    """
    RideEvent model for tracking events during a ride.
    Important: This table will be very large, so we need to optimize queries.
    """
    id_ride_event = models.AutoField(primary_key=True)
    id_ride = models.ForeignKey(
        Ride,
        on_delete=models.CASCADE,
        related_name='ride_events',
        db_column='id_ride'
    )
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ride_event'
        indexes = [
            models.Index(fields=['id_ride', 'created_at']),
            models.Index(fields=['created_at']),
            models.Index(fields=['description']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"Event {self.id_ride_event} - {self.description}"
