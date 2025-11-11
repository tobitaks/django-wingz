# Wingz Ride Management API

A RESTful API built with Django REST Framework for managing ride-sharing information, with a strong focus on performance optimization and efficient database query patterns.

## Features

- **Full CRUD API** for Rides, Users, and Ride Events
- **Performance Optimized**: Achieves 2-3 database queries for ride list endpoint
- **Advanced Filtering**: Filter by ride status and rider email
- **Smart Sorting**: Sort by pickup time or GPS distance from any location
- **Pagination**: Built-in pagination for all list endpoints
- **Admin Authentication**: Role-based access control for admin users
- **Docker Setup**: Complete containerized development environment
- **Sample Data Generator**: Command to generate realistic test data
- **Bonus SQL Query**: Complex reporting query for trip duration analysis

## Tech Stack

- **Backend**: Python 3.10, Django 5.0, Django REST Framework 3.14
- **Database**: PostgreSQL 15
- **Containerization**: Docker, Docker Compose
- **Development Tools**: Django Debug Toolbar, Makefile

## Project Structure

```
djagno-assessment/
├── config/                 # Django project settings
│   ├── settings.py        # Main settings with REST Framework config
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py
├── rides/                 # Main application
│   ├── models.py          # User, Ride, RideEvent models
│   ├── serializers.py     # DRF serializers with optimization
│   ├── views.py           # ViewSets with query optimization
│   ├── permissions.py     # IsAdminUser permission class
│   ├── filters.py         # Custom filter for rides
│   ├── admin.py           # Django admin configuration
│   ├── urls.py            # API routes
│   └── management/
│       └── commands/
│           └── generate_sample_data.py
├── docker-compose.yml     # Docker services configuration
├── Dockerfile             # Django container definition
├── Makefile               # Common commands
├── requirements/          # Python dependencies
│   ├── base.txt          # Production dependencies
│   └── development.txt   # Development dependencies
├── PROJECT_PLAN.md        # Detailed project plan
└── README.md              # This file
```

## Quick Start

### Prerequisites
- Docker and Docker Compose installed

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd djagno-assessment

# Build and start containers
make build
make start-bg

# Run migrations
make migrate

# Create superuser for admin access
make createsuperuser

# Generate sample data
make manage ARGS='generate_sample_data'
```

### Access the Application

- **API Root**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **Rides Endpoint**: http://localhost:8000/api/rides/

## API Documentation

### Authentication

All API endpoints require authentication. Login via the admin panel or DRF browsable API. Only users with `role='admin'` (or Django superusers) can access the API.

### Endpoints

#### List Rides
```
GET /api/rides/
```

**Query Parameters:**
- `page` - Page number for pagination
- `status` - Filter by ride status (`en-route`, `pickup`, `dropoff`)
- `rider_email` - Filter by rider email (case-insensitive)
- `ordering` - Sort by `pickup_time` (use `-pickup_time` for descending)
- `latitude` & `longitude` - Sort by GPS distance

**Example Requests:**
```bash
GET /api/rides/?status=pickup
GET /api/rides/?rider_email=rider0@example.com
GET /api/rides/?latitude=37.75&longitude=-122.45
GET /api/rides/?status=dropoff&page=2
```

#### Create Ride
```
POST /api/rides/
```

**Request Body:**
```json
{
  "status": "en-route",
  "id_rider_id": 1,
  "id_driver_id": 11,
  "pickup_latitude": 37.7749,
  "pickup_longitude": -122.4194,
  "dropoff_latitude": 37.7849,
  "dropoff_longitude": -122.4094,
  "pickup_time": "2025-11-10T10:30:00Z"
}
```

#### Other Endpoints

- `GET/POST /api/users/` - List/Create users
- `GET/PUT/PATCH/DELETE /api/users/{id}/` - User detail
- `GET/POST /api/ride-events/` - List/Create ride events
- `GET/PUT/PATCH/DELETE /api/ride-events/{id}/` - Ride event detail

## Performance Optimization

### Query Optimization Strategy

The Ride List API achieves the **2-3 query target** through:

1. **select_related()** for ForeignKey relationships (rider, driver)
2. **prefetch_related()** with custom Prefetch for reverse FK (ride_events)
3. **Filtered prefetch** to only fetch events from last 24 hours

### Verified Performance

**Query Breakdown** (verified with Django Debug Toolbar):
- Query 1: Pagination count
- Query 2: Main query with JOINs for rider and driver
- Query 3: Prefetch query for today's ride events

**Total Response Time**: ~4.5ms for ride list with full nested data

### Code Implementation

```python
# rides/views.py
def get_queryset(self):
    cutoff_time = timezone.now() - timedelta(hours=24)

    todays_events_prefetch = Prefetch(
        'ride_events',
        queryset=RideEvent.objects.filter(created_at__gte=cutoff_time),
        to_attr='todays_ride_events_prefetch'
    )

    queryset = Ride.objects.select_related(
        'id_rider',
        'id_driver'
    ).prefetch_related(
        todays_events_prefetch
    )

    return queryset
```

## Bonus SQL Query - Trips Over 1 Hour

Reports trips that took more than 1 hour from pickup to dropoff, grouped by month and driver.

### SQL Query

```sql
WITH ride_durations AS (
    SELECT
        r.id_ride,
        r.id_driver,
        u.first_name || ' ' || SUBSTRING(u.last_name, 1, 1) AS driver_name,
        MIN(CASE
            WHEN re.description = 'Status changed to pickup'
            THEN re.created_at
        END) AS pickup_time,
        MAX(CASE
            WHEN re.description = 'Status changed to dropoff'
            THEN re.created_at
        END) AS dropoff_time
    FROM
        ride r
        INNER JOIN "user" u ON r.id_driver = u.id_user
        INNER JOIN ride_event re ON r.id_ride = re.id_ride
    WHERE
        re.description IN ('Status changed to pickup', 'Status changed to dropoff')
    GROUP BY
        r.id_ride, r.id_driver, u.first_name, u.last_name
    HAVING
        MIN(CASE WHEN re.description = 'Status changed to pickup' THEN re.created_at END) IS NOT NULL
        AND MAX(CASE WHEN re.description = 'Status changed to dropoff' THEN re.created_at END) IS NOT NULL
)
SELECT
    TO_CHAR(pickup_time, 'YYYY-MM') AS month,
    driver_name AS driver,
    COUNT(*) AS "count_of_trips_gt_1hr"
FROM
    ride_durations
WHERE
    EXTRACT(EPOCH FROM (dropoff_time - pickup_time)) / 3600 > 1
GROUP BY
    TO_CHAR(pickup_time, 'YYYY-MM'),
    driver_name
ORDER BY
    month ASC,
    driver_name ASC;
```

### How to Run

```bash
# Access database shell
make dbshell

# Paste the SQL query above
```

### Query Explanation

1. **CTE (ride_durations)**: Uses conditional aggregation to find pickup and dropoff event times
2. **Duration Calculation**: Converts time difference to hours using `EXTRACT(EPOCH ...)`
3. **Filtering**: `WHERE ... > 1` filters for trips longer than 1 hour
4. **Grouping**: Groups by month (YYYY-MM format) and driver name

## Development Commands

```bash
# Container Management
make build              # Build Docker containers
make start-bg           # Start containers (background)
make stop               # Stop containers
make restart            # Restart containers
make logs               # View container logs

# Database
make migrate            # Run migrations
make dbshell            # Open PostgreSQL shell

# Django
make shell              # Open Django shell
make createsuperuser    # Create superuser
make manage ARGS='...'  # Run any manage.py command

# Data
make manage ARGS='generate_sample_data'              # Generate 100 rides
make manage ARGS='generate_sample_data --rides=50'   # Generate 50 rides
make manage ARGS='flush --no-input'                  # Clear all data
```

## Requirements Met

✅ Django REST Framework with ViewSets
✅ Models: User, Ride, RideEvent
✅ Serializers with nested relations
✅ Admin-only authentication
✅ Filtering (status, rider email)
✅ Sorting (pickup_time, GPS distance)
✅ Pagination support
✅ Performance optimization (2-3 queries)
✅ `todays_ride_events` field (last 24 hours only)
✅ Bonus SQL query for trips > 1 hour

---

Built as part of the Wingz Django Engineer assessment.
