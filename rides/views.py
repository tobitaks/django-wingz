from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Prefetch, Q
from django.utils import timezone
from datetime import timedelta

from .models import User, Ride, RideEvent
from .serializers import UserSerializer, RideSerializer, RideListSerializer, RideEventSerializer
from .permissions import IsAdminUser
from .filters import RideFilter


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model.
    Only accessible by admin users.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['email', 'first_name', 'last_name']
    ordering_fields = ['id_user', 'email', 'role']


class RideViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Ride model with optimized queries.

    Performance optimizations:
    1. Uses select_related() for rider and driver ForeignKeys (1 query)
    2. Uses prefetch_related() with custom Prefetch for today's ride events (1 query)
    3. Total: 2-3 queries (including pagination count)

    Features:
    - Filtering by status and rider email
    - Sorting by pickup_time and distance to pickup location
    - Pagination
    - Admin-only access
    """
    serializer_class = RideListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = RideFilter
    ordering_fields = ['pickup_time']
    ordering = ['-pickup_time']

    def get_queryset(self):
        """
        Optimized queryset with select_related and prefetch_related.

        This achieves the 2-query target:
        1. Main query with select_related for rider and driver
        2. Prefetch query for today's ride events
        (3rd query is for pagination count)
        """
        # Calculate 24 hours ago for today's events filter
        cutoff_time = timezone.now() - timedelta(hours=24)

        # Create a custom prefetch for today's ride events only
        todays_events_prefetch = Prefetch(
            'ride_events',
            queryset=RideEvent.objects.filter(created_at__gte=cutoff_time).order_by('-created_at'),
            to_attr='todays_ride_events_prefetch'
        )

        # Build the optimized queryset
        queryset = Ride.objects.select_related(
            'id_rider',   # ForeignKey to User (rider)
            'id_driver'   # ForeignKey to User (driver)
        ).prefetch_related(
            todays_events_prefetch  # Only today's events
        )

        # Handle GPS-based distance sorting if provided
        lat = self.request.query_params.get('latitude')
        lon = self.request.query_params.get('longitude')

        if lat and lon:
            try:
                lat = float(lat)
                lon = float(lon)
                # Add distance annotation and ordering
                # Using Haversine formula approximation
                from django.db.models import F, FloatField
                from django.db.models.functions import ACos, Cos, Radians, Sin

                # Haversine formula for distance calculation
                # This is database-level calculation for efficiency
                queryset = queryset.annotate(
                    distance=ACos(
                        Cos(Radians(lat)) *
                        Cos(Radians(F('pickup_latitude'))) *
                        Cos(Radians(F('pickup_longitude')) - Radians(lon)) +
                        Sin(Radians(lat)) *
                        Sin(Radians(F('pickup_latitude')))
                    ) * 6371  # Earth's radius in km
                ).order_by('distance')
            except (ValueError, TypeError):
                pass  # Invalid coordinates, ignore distance sorting

        return queryset

    def get_serializer_class(self):
        """
        Use different serializers for list and detail views.
        """
        if self.action == 'list':
            return RideListSerializer
        return RideSerializer


class RideEventViewSet(viewsets.ModelViewSet):
    """
    ViewSet for RideEvent model.
    Only accessible by admin users.
    """
    queryset = RideEvent.objects.select_related('id_ride').all()
    serializer_class = RideEventSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['id_ride', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
