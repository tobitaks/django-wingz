from rest_framework import serializers
from .models import User, Ride, RideEvent
from django.utils import timezone
from datetime import timedelta


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    Used for nested representation in Ride serializer.
    """
    class Meta:
        model = User
        fields = ['id_user', 'role', 'first_name', 'last_name', 'email', 'phone_number']
        read_only_fields = ['id_user']


class RideEventSerializer(serializers.ModelSerializer):
    """
    Serializer for RideEvent model.
    """
    class Meta:
        model = RideEvent
        fields = ['id_ride_event', 'id_ride', 'description', 'created_at']
        read_only_fields = ['id_ride_event', 'created_at']


class RideSerializer(serializers.ModelSerializer):
    """
    Serializer for Ride model with nested relations.

    This serializer includes:
    - Full rider and driver details (nested)
    - All ride events (will be optimized with prefetch_related)
    - Today's ride events (only events from last 24 hours)
    """
    # Nested serializers for rider and driver
    rider = UserSerializer(source='id_rider', read_only=True)
    driver = UserSerializer(source='id_driver', read_only=True)

    # All ride events (will be prefetched)
    ride_events = RideEventSerializer(many=True, read_only=True)

    # Today's ride events (only last 24 hours) - will be populated via prefetch
    todays_ride_events = serializers.SerializerMethodField()

    # Write-only fields for creating/updating rides
    id_rider_id = serializers.IntegerField(write_only=True, required=False)
    id_driver_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = Ride
        fields = [
            'id_ride',
            'status',
            'id_rider_id',  # write-only
            'id_driver_id',  # write-only
            'rider',  # read-only nested
            'driver',  # read-only nested
            'pickup_latitude',
            'pickup_longitude',
            'dropoff_latitude',
            'dropoff_longitude',
            'pickup_time',
            'ride_events',  # all events
            'todays_ride_events',  # filtered events
        ]
        read_only_fields = ['id_ride']

    def get_todays_ride_events(self, obj):
        """
        Get ride events from the last 24 hours.

        This will use the prefetched 'todays_ride_events' if available,
        otherwise it will query the database (which we want to avoid).

        The prefetch will be done in the ViewSet to minimize queries.
        """
        # Check if we have prefetched data
        if hasattr(obj, 'todays_ride_events_prefetch'):
            events = obj.todays_ride_events_prefetch
        else:
            # Fallback (not ideal - should use prefetch in ViewSet)
            cutoff_time = timezone.now() - timedelta(hours=24)
            events = obj.ride_events.filter(created_at__gte=cutoff_time)

        return RideEventSerializer(events, many=True).data


class RideListSerializer(serializers.ModelSerializer):
    """
    Optimized serializer for list view.
    Same as RideSerializer but designed for efficient bulk queries.
    """
    rider = UserSerializer(source='id_rider', read_only=True)
    driver = UserSerializer(source='id_driver', read_only=True)
    todays_ride_events = serializers.SerializerMethodField()

    class Meta:
        model = Ride
        fields = [
            'id_ride',
            'status',
            'rider',
            'driver',
            'pickup_latitude',
            'pickup_longitude',
            'dropoff_latitude',
            'dropoff_longitude',
            'pickup_time',
            'todays_ride_events',
        ]

    def get_todays_ride_events(self, obj):
        """
        Get today's ride events using prefetched data.
        """
        if hasattr(obj, 'todays_ride_events_prefetch'):
            events = obj.todays_ride_events_prefetch
        else:
            cutoff_time = timezone.now() - timedelta(hours=24)
            events = obj.ride_events.filter(created_at__gte=cutoff_time)

        return RideEventSerializer(events, many=True).data
