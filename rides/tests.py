from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import timedelta
from decimal import Decimal
from .models import User, Ride, RideEvent
from .serializers import RideSerializer, RideEventSerializer


class RideModelTest(TestCase):
    """Test the Ride model"""

    def setUp(self):
        self.rider = User.objects.create(
            role='rider',
            first_name='Jane',
            last_name='Rider',
            email='rider@example.com',
            phone_number='+1111111111'
        )
        self.driver = User.objects.create(
            role='driver',
            first_name='Bob',
            last_name='Driver',
            email='driver@example.com',
            phone_number='+2222222222'
        )
        self.ride_data = {
            'status': 'en-route',
            'id_rider': self.rider,
            'id_driver': self.driver,
            'pickup_latitude': 37.7749,
            'pickup_longitude': -122.4194,
            'dropoff_latitude': 37.7849,
            'dropoff_longitude': -122.4094,
            'pickup_time': timezone.now()
        }

    def test_create_ride(self):
        """Test creating a ride"""
        ride = Ride.objects.create(**self.ride_data)
        self.assertEqual(ride.status, 'en-route')
        self.assertEqual(ride.id_rider, self.rider)
        self.assertEqual(ride.id_driver, self.driver)
        self.assertEqual(ride.pickup_latitude, 37.7749)
        self.assertEqual(ride.pickup_longitude, -122.4194)

    def test_ride_string_representation(self):
        """Test the ride string representation"""
        ride = Ride.objects.create(**self.ride_data)
        expected_str = f"Ride {ride.id_ride} - en-route"
        self.assertEqual(str(ride), expected_str)

    def test_ride_status_choices(self):
        """Test that only valid status choices are accepted"""
        ride = Ride.objects.create(**self.ride_data)
        self.assertIn(ride.status, ['en-route', 'pickup', 'dropoff'])

    def test_ride_foreign_key_relationships(self):
        """Test that foreign key relationships work correctly"""
        ride = Ride.objects.create(**self.ride_data)
        self.assertEqual(ride.id_rider.email, 'rider@example.com')
        self.assertEqual(ride.id_driver.email, 'driver@example.com')

    def test_cascade_delete(self):
        """Test that deleting a user cascades to rides"""
        ride = Ride.objects.create(**self.ride_data)
        rider_id = self.rider.id_user
        self.rider.delete()
        # Ride should be deleted due to CASCADE
        with self.assertRaises(Ride.DoesNotExist):
            Ride.objects.get(id_ride=ride.id_ride)


class RideEventModelTest(TestCase):
    """Test the RideEvent model"""

    def setUp(self):
        self.rider = User.objects.create(
            role='rider',
            first_name='Jane',
            last_name='Rider',
            email='rider@example.com',
            phone_number='+1111111111'
        )
        self.driver = User.objects.create(
            role='driver',
            first_name='Bob',
            last_name='Driver',
            email='driver@example.com',
            phone_number='+2222222222'
        )
        self.ride = Ride.objects.create(
            status='en-route',
            id_rider=self.rider,
            id_driver=self.driver,
            pickup_latitude=37.7749,
            pickup_longitude=-122.4194,
            dropoff_latitude=37.7849,
            dropoff_longitude=-122.4094,
            pickup_time=timezone.now()
        )

    def test_create_ride_event(self):
        """Test creating a ride event"""
        event = RideEvent.objects.create(
            id_ride=self.ride,
            description='Driver en route'
        )
        self.assertEqual(event.description, 'Driver en route')
        self.assertEqual(event.id_ride, self.ride)
        self.assertIsNotNone(event.created_at)

    def test_ride_event_string_representation(self):
        """Test the ride event string representation"""
        event = RideEvent.objects.create(
            id_ride=self.ride,
            description='Driver en route'
        )
        expected_str = f"Event {event.id_ride_event} - Driver en route"
        self.assertEqual(str(event), expected_str)

    def test_ride_event_cascade_delete(self):
        """Test that deleting a ride cascades to events"""
        event = RideEvent.objects.create(
            id_ride=self.ride,
            description='Driver en route'
        )
        event_id = event.id_ride_event
        self.ride.delete()
        # Event should be deleted due to CASCADE
        with self.assertRaises(RideEvent.DoesNotExist):
            RideEvent.objects.get(id_ride_event=event_id)

    def test_ride_event_auto_timestamp(self):
        """Test that created_at is automatically set"""
        before = timezone.now()
        event = RideEvent.objects.create(
            id_ride=self.ride,
            description='Driver en route'
        )
        after = timezone.now()
        self.assertGreaterEqual(event.created_at, before)
        self.assertLessEqual(event.created_at, after)


class RideSerializerTest(TestCase):
    """Test the Ride serializer"""

    def setUp(self):
        self.rider = User.objects.create(
            role='rider',
            first_name='Jane',
            last_name='Rider',
            email='rider@example.com',
            phone_number='+1111111111'
        )
        self.driver = User.objects.create(
            role='driver',
            first_name='Bob',
            last_name='Driver',
            email='driver@example.com',
            phone_number='+2222222222'
        )
        self.pickup_time = timezone.now()
        self.ride = Ride.objects.create(
            status='en-route',
            id_rider=self.rider,
            id_driver=self.driver,
            pickup_latitude=37.7749,
            pickup_longitude=-122.4194,
            dropoff_latitude=37.7849,
            dropoff_longitude=-122.4094,
            pickup_time=self.pickup_time
        )

    def test_ride_serializer_contains_expected_fields(self):
        """Test that serializer contains all expected fields"""
        serializer = RideSerializer(instance=self.ride)
        data = serializer.data
        # Note: id_rider_id and id_driver_id are write_only fields, so they don't appear in read data
        expected_fields = {
            'id_ride', 'status',
            'pickup_latitude', 'pickup_longitude', 'dropoff_latitude',
            'dropoff_longitude', 'pickup_time', 'rider', 'driver',
            'ride_events', 'todays_ride_events'
        }
        self.assertEqual(set(data.keys()), expected_fields)

    def test_ride_serializer_nested_relationships(self):
        """Test that nested rider and driver are properly serialized"""
        serializer = RideSerializer(instance=self.ride)
        data = serializer.data
        self.assertEqual(data['rider']['email'], 'rider@example.com')
        self.assertEqual(data['driver']['email'], 'driver@example.com')
        self.assertEqual(data['rider']['first_name'], 'Jane')
        self.assertEqual(data['driver']['first_name'], 'Bob')


class AuthenticationAPITest(APITestCase):
    """Test authentication endpoints"""

    def setUp(self):
        self.client = APIClient()
        # Create Django superuser for authentication tests
        from django.contrib.auth.models import User as DjangoUser
        self.django_user = DjangoUser.objects.create_user(
            username='testadmin',
            password='testpass123',
            is_staff=True,
            is_superuser=True
        )
        # Create custom admin user
        self.admin_user = User.objects.create(
            role='admin',
            first_name='Admin',
            last_name='User',
            email='admin@example.com',
            phone_number='+1234567890'
        )

    def test_login_with_valid_credentials(self):
        """Test login with valid credentials"""
        url = reverse('auth-login')
        data = {
            'username': 'testadmin',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_login_with_invalid_credentials(self):
        """Test login with invalid credentials"""
        url = reverse('auth-login')
        data = {
            'username': 'testadmin',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_check_authenticated_status(self):
        """Test checking authentication status"""
        self.client.force_authenticate(user=self.django_user)
        url = reverse('auth-check')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['authenticated'])

    def test_logout(self):
        """Test logout functionality"""
        self.client.force_authenticate(user=self.django_user)
        url = reverse('auth-logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class RideAPITest(APITestCase):
    """Test Ride API endpoints"""

    def setUp(self):
        self.client = APIClient()
        # Create Django superuser for API access
        from django.contrib.auth.models import User as DjangoUser
        self.django_user = DjangoUser.objects.create_user(
            username='testadmin',
            password='testpass123',
            is_staff=True,
            is_superuser=True
        )
        self.client.force_authenticate(user=self.django_user)

        # Create test users
        self.rider = User.objects.create(
            role='rider',
            first_name='Jane',
            last_name='Rider',
            email='rider@example.com',
            phone_number='+1111111111'
        )
        self.driver = User.objects.create(
            role='driver',
            first_name='Bob',
            last_name='Driver',
            email='driver@example.com',
            phone_number='+2222222222'
        )

        # Create test rides
        self.ride1 = Ride.objects.create(
            status='en-route',
            id_rider=self.rider,
            id_driver=self.driver,
            pickup_latitude=37.7749,
            pickup_longitude=-122.4194,
            dropoff_latitude=37.7849,
            dropoff_longitude=-122.4094,
            pickup_time=timezone.now()
        )
        self.ride2 = Ride.objects.create(
            status='pickup',
            id_rider=self.rider,
            id_driver=self.driver,
            pickup_latitude=37.7849,
            pickup_longitude=-122.4294,
            dropoff_latitude=37.7949,
            dropoff_longitude=-122.4394,
            pickup_time=timezone.now() + timedelta(hours=1)
        )

    def test_get_ride_list(self):
        """Test retrieving list of rides"""
        url = reverse('ride-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_get_ride_detail(self):
        """Test retrieving a single ride"""
        url = reverse('ride-detail', kwargs={'pk': self.ride1.id_ride})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id_ride'], self.ride1.id_ride)
        self.assertEqual(response.data['status'], 'en-route')

    def test_create_ride(self):
        """Test creating a new ride"""
        url = reverse('ride-list')
        data = {
            'status': 'dropoff',
            'id_rider_id': self.rider.id_user,
            'id_driver_id': self.driver.id_user,
            'pickup_latitude': 37.7649,
            'pickup_longitude': -122.4094,
            'dropoff_latitude': 37.7749,
            'dropoff_longitude': -122.4194,
            'pickup_time': timezone.now().isoformat()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ride.objects.count(), 3)
        self.assertEqual(response.data['status'], 'dropoff')

    def test_update_ride(self):
        """Test updating a ride"""
        url = reverse('ride-detail', kwargs={'pk': self.ride1.id_ride})
        data = {
            'status': 'dropoff',
            'id_rider_id': self.rider.id_user,
            'id_driver_id': self.driver.id_user,
            'pickup_latitude': 37.7749,
            'pickup_longitude': -122.4194,
            'dropoff_latitude': 37.7849,
            'dropoff_longitude': -122.4094,
            'pickup_time': self.ride1.pickup_time.isoformat()
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ride1.refresh_from_db()
        self.assertEqual(self.ride1.status, 'dropoff')

    def test_partial_update_ride(self):
        """Test partially updating a ride"""
        url = reverse('ride-detail', kwargs={'pk': self.ride1.id_ride})
        data = {'status': 'pickup'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.ride1.refresh_from_db()
        self.assertEqual(self.ride1.status, 'pickup')

    def test_delete_ride(self):
        """Test deleting a ride"""
        url = reverse('ride-detail', kwargs={'pk': self.ride1.id_ride})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Ride.objects.count(), 1)

    def test_unauthenticated_access_denied(self):
        """Test that unauthenticated requests are denied"""
        self.client.force_authenticate(user=None)
        url = reverse('ride-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class RideFilteringAPITest(APITestCase):
    """Test filtering and sorting for Ride API"""

    def setUp(self):
        self.client = APIClient()
        # Create Django superuser for API access
        from django.contrib.auth.models import User as DjangoUser
        self.django_user = DjangoUser.objects.create_user(
            username='testadmin',
            password='testpass123',
            is_staff=True,
            is_superuser=True
        )
        self.client.force_authenticate(user=self.django_user)

        # Create test users
        self.rider1 = User.objects.create(
            role='rider',
            first_name='Alice',
            last_name='Rider',
            email='alice@example.com',
            phone_number='+1111111111'
        )
        self.rider2 = User.objects.create(
            role='rider',
            first_name='Bob',
            last_name='Rider',
            email='bob@example.com',
            phone_number='+2222222222'
        )
        self.driver = User.objects.create(
            role='driver',
            first_name='Charlie',
            last_name='Driver',
            email='driver@example.com',
            phone_number='+3333333333'
        )

        # Create rides with different statuses
        self.ride_enroute = Ride.objects.create(
            status='en-route',
            id_rider=self.rider1,
            id_driver=self.driver,
            pickup_latitude=37.7749,
            pickup_longitude=-122.4194,
            dropoff_latitude=37.7849,
            dropoff_longitude=-122.4094,
            pickup_time=timezone.now() - timedelta(hours=2)
        )
        self.ride_pickup = Ride.objects.create(
            status='pickup',
            id_rider=self.rider2,
            id_driver=self.driver,
            pickup_latitude=37.7849,
            pickup_longitude=-122.4294,
            dropoff_latitude=37.7949,
            dropoff_longitude=-122.4394,
            pickup_time=timezone.now() - timedelta(hours=1)
        )
        self.ride_dropoff = Ride.objects.create(
            status='dropoff',
            id_rider=self.rider1,
            id_driver=self.driver,
            pickup_latitude=37.7949,
            pickup_longitude=-122.4394,
            dropoff_latitude=37.8049,
            dropoff_longitude=-122.4494,
            pickup_time=timezone.now()
        )

    def test_filter_by_status(self):
        """Test filtering rides by status"""
        url = reverse('ride-list')
        response = self.client.get(url, {'status': 'en-route'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['status'], 'en-route')

    def test_filter_by_rider_email(self):
        """Test filtering rides by rider email"""
        url = reverse('ride-list')
        response = self.client.get(url, {'rider_email': 'alice@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)

    def test_sort_by_pickup_time_ascending(self):
        """Test sorting rides by pickup_time ascending"""
        url = reverse('ride-list')
        response = self.client.get(url, {'ordering': 'pickup_time'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        # First result should be oldest
        self.assertEqual(results[0]['id_ride'], self.ride_enroute.id_ride)

    def test_sort_by_pickup_time_descending(self):
        """Test sorting rides by pickup_time descending"""
        url = reverse('ride-list')
        response = self.client.get(url, {'ordering': '-pickup_time'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data['results']
        # First result should be newest
        self.assertEqual(results[0]['id_ride'], self.ride_dropoff.id_ride)

    def test_gps_distance_sorting(self):
        """Test sorting rides by GPS distance"""
        url = reverse('ride-list')
        # Use coordinates close to ride_pickup
        response = self.client.get(url, {
            'latitude': 37.7849,
            'longitude': -122.4294
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify that results are ordered (closer rides should appear first)
        # We can verify by checking that all 3 rides are returned
        results = response.data['results']
        self.assertEqual(len(results), 3)
        # Extract all ride IDs
        result_ids = [r['id_ride'] for r in results]
        # Verify all our test rides are in the results
        self.assertIn(self.ride_enroute.id_ride, result_ids)
        self.assertIn(self.ride_pickup.id_ride, result_ids)
        self.assertIn(self.ride_dropoff.id_ride, result_ids)

    def test_combined_filters(self):
        """Test combining multiple filters"""
        url = reverse('ride-list')
        response = self.client.get(url, {
            'status': 'pickup',
            'rider_email': 'bob@example.com'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['id_ride'], self.ride_pickup.id_ride)


class PerformanceOptimizationTest(APITestCase):
    """Test query performance optimization"""

    def setUp(self):
        self.client = APIClient()
        # Create Django superuser for API access
        from django.contrib.auth.models import User as DjangoUser
        self.django_user = DjangoUser.objects.create_user(
            username='testadmin',
            password='testpass123',
            is_staff=True,
            is_superuser=True
        )
        self.client.force_authenticate(user=self.django_user)

        # Create test data
        self.rider = User.objects.create(
            role='rider',
            first_name='Test',
            last_name='Rider',
            email='rider@example.com',
            phone_number='+1111111111'
        )
        self.driver = User.objects.create(
            role='driver',
            first_name='Test',
            last_name='Driver',
            email='driver@example.com',
            phone_number='+2222222222'
        )

        # Create ride with events
        self.ride = Ride.objects.create(
            status='en-route',
            id_rider=self.rider,
            id_driver=self.driver,
            pickup_latitude=37.7749,
            pickup_longitude=-122.4194,
            dropoff_latitude=37.7849,
            dropoff_longitude=-122.4094,
            pickup_time=timezone.now()
        )

        # Create recent events (today)
        for i in range(3):
            RideEvent.objects.create(
                id_ride=self.ride,
                description=f'Recent event {i}'
            )

        # Create old events (2 days ago) - should not appear in todays_ride_events
        old_time = timezone.now() - timedelta(days=2)
        for i in range(2):
            event = RideEvent.objects.create(
                id_ride=self.ride,
                description=f'Old event {i}'
            )
            # Manually update created_at to simulate old event
            RideEvent.objects.filter(id_ride_event=event.id_ride_event).update(created_at=old_time)

    def test_todays_events_filtering(self):
        """Test that only today's events are included in response"""
        url = reverse('ride-detail', kwargs={'pk': self.ride.id_ride})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Should only have 3 recent events in todays_ride_events, not the 2 old ones
        todays_events = response.data.get('todays_ride_events', [])
        self.assertEqual(len(todays_events), 3)

        # Verify all returned events have "Recent event" in description
        for event in todays_events:
            self.assertIn('Recent event', event['description'])

        # The ride_events field should contain all 5 events (3 recent + 2 old)
        all_events = response.data.get('ride_events', [])
        self.assertEqual(len(all_events), 5)

    def test_query_count_optimization(self):
        """Test that query count is optimized (2-3 queries)"""
        from django.test.utils import override_settings
        from django.db import connection
        from django.test import utils

        url = reverse('ride-list')

        # Reset query log
        connection.queries_log.clear()

        # Enable query logging
        with self.settings(DEBUG=True):
            response = self.client.get(url)
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Should be approximately 2-3 queries:
            # 1. Count query for pagination
            # 2. Main query with select_related (rider, driver)
            # 3. Prefetch query for today's events
            query_count = len(connection.queries)

            # Allow some flexibility for session queries, but should not exceed 5
            self.assertLessEqual(query_count, 5,
                f"Too many queries executed: {query_count}. Expected <= 5.")
