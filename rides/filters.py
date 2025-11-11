import django_filters
from .models import Ride


class RideFilter(django_filters.FilterSet):
    """
    Custom filter for Ride model.

    Supports:
    - Filtering by status (exact match)
    - Filtering by rider email (exact match or icontains)
    """
    status = django_filters.CharFilter(field_name='status', lookup_expr='exact')
    rider_email = django_filters.CharFilter(field_name='id_rider__email', lookup_expr='icontains')

    class Meta:
        model = Ride
        fields = ['status', 'rider_email']
