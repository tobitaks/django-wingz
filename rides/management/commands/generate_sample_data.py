from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from rides.models import User, Ride, RideEvent


class Command(BaseCommand):
    help = 'Generate sample data for testing the Ride API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=20,
            help='Number of users to create (riders and drivers)'
        )
        parser.add_argument(
            '--rides',
            type=int,
            default=100,
            help='Number of rides to create'
        )
        parser.add_argument(
            '--events-per-ride',
            type=int,
            default=5,
            help='Average number of events per ride'
        )

    def handle(self, *args, **options):
        num_users = options['users']
        num_rides = options['rides']
        events_per_ride = options['events_per_ride']

        self.stdout.write(self.style.SUCCESS('Starting data generation...'))

        # Create admin user if not exists
        admin, created = User.objects.get_or_create(
            email='admin@wingz.com',
            defaults={
                'role': 'admin',
                'first_name': 'Admin',
                'last_name': 'User',
                'phone_number': '+1234567890'
            }
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created admin user: {admin.email}'))

        # Create riders
        riders = []
        for i in range(num_users // 2):
            rider, created = User.objects.get_or_create(
                email=f'rider{i}@example.com',
                defaults={
                    'role': 'rider',
                    'first_name': f'Rider{i}',
                    'last_name': f'User{i}',
                    'phone_number': f'+1555{i:04d}'
                }
            )
            riders.append(rider)

        self.stdout.write(self.style.SUCCESS(f'Created {len(riders)} riders'))

        # Create drivers
        drivers = []
        for i in range(num_users // 2):
            driver, created = User.objects.get_or_create(
                email=f'driver{i}@example.com',
                defaults={
                    'role': 'driver',
                    'first_name': f'Driver{i}',
                    'last_name': f'User{i}',
                    'phone_number': f'+1666{i:04d}'
                }
            )
            drivers.append(driver)

        self.stdout.write(self.style.SUCCESS(f'Created {len(drivers)} drivers'))

        # Create rides
        statuses = ['en-route', 'pickup', 'dropoff']

        # San Francisco area coordinates for realistic data
        sf_lat_range = (37.7, 37.8)
        sf_lon_range = (-122.5, -122.4)

        for i in range(num_rides):
            # Random time within last 30 days
            days_ago = random.randint(0, 30)
            hours_ago = random.randint(0, 23)
            pickup_time = timezone.now() - timedelta(days=days_ago, hours=hours_ago)

            ride = Ride.objects.create(
                status=random.choice(statuses),
                id_rider=random.choice(riders),
                id_driver=random.choice(drivers),
                pickup_latitude=random.uniform(*sf_lat_range),
                pickup_longitude=random.uniform(*sf_lon_range),
                dropoff_latitude=random.uniform(*sf_lat_range),
                dropoff_longitude=random.uniform(*sf_lon_range),
                pickup_time=pickup_time
            )

            # Create ride events
            # First, create the essential pickup and dropoff events for the SQL query
            pickup_event_time = pickup_time + timedelta(minutes=random.randint(5, 15))
            pickup_event = RideEvent(
                id_ride=ride,
                description='Status changed to pickup'
            )
            pickup_event.save()
            RideEvent.objects.filter(id_ride_event=pickup_event.id_ride_event).update(
                created_at=pickup_event_time
            )

            # Dropoff event happens 30 minutes to 3 hours after pickup
            # This ensures we have some trips > 1 hour and some < 1 hour
            trip_duration_minutes = random.randint(30, 180)
            dropoff_event_time = pickup_event_time + timedelta(minutes=trip_duration_minutes)
            dropoff_event = RideEvent(
                id_ride=ride,
                description='Status changed to dropoff'
            )
            dropoff_event.save()
            RideEvent.objects.filter(id_ride_event=dropoff_event.id_ride_event).update(
                created_at=dropoff_event_time
            )

            # Create additional random events
            other_event_descriptions = [
                'Ride requested',
                'Driver assigned',
                'Driver en route',
                'Passenger picked up',
                'En route to destination',
                'Passenger dropped off',
                'Ride completed',
                'Payment processed'
            ]

            num_other_events = random.randint(2, 5)
            for j in range(num_other_events):
                # Events happen between pickup_time and dropoff_event_time
                minutes_offset = random.randint(0, trip_duration_minutes + 20)
                event_time = pickup_time + timedelta(minutes=minutes_offset)

                event = RideEvent(
                    id_ride=ride,
                    description=random.choice(other_event_descriptions)
                )
                event.save()
                RideEvent.objects.filter(id_ride_event=event.id_ride_event).update(
                    created_at=event_time
                )

        self.stdout.write(self.style.SUCCESS(f'Created {num_rides} rides with events'))

        # Summary
        total_events = RideEvent.objects.count()
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('Data generation complete!'))
        self.stdout.write(self.style.SUCCESS(f'Total Users: {User.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total Rides: {Ride.objects.count()}'))
        self.stdout.write(self.style.SUCCESS(f'Total Events: {total_events}'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.WARNING('\nAdmin user credentials:'))
        self.stdout.write(self.style.WARNING(f'Email: admin@wingz.com'))
        self.stdout.write(self.style.WARNING('(Use Django superuser for admin login)'))
