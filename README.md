# Wingz Ride Management API

A RESTful API built with Django REST Framework for managing ride-sharing information, with a strong focus on performance optimization and efficient database query patterns.

## 🚀 Features

- **Full CRUD API** for Rides, Users, and Ride Events
- **Performance Optimized**: Achieves 2-3 database queries for ride list endpoint
- **Advanced Filtering**: Filter by ride status and rider email
- **Smart Sorting**: Sort by pickup time or GPS distance from any location
- **Pagination**: Built-in pagination for all list endpoints
- **Admin Authentication**: Role-based access control for admin users
- **Docker Setup**: Complete containerized development environment
- **Sample Data Generator**: Command to generate realistic test data
- **Bonus SQL Query**: Complex reporting query for trip duration analysis

## 📋 Requirements Met

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

## 🛠️ Tech Stack

- **Backend**: Python 3.10, Django 5.0, Django REST Framework 3.14
- **Database**: PostgreSQL 15
- **Containerization**: Docker, Docker Compose
- **API Documentation**: DRF Browsable API
- **Development Tools**: Django Debug Toolbar, Makefile

## 📦 Project Structure

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
├── Makefile              # Common commands
├── requirements.txt       # Python dependencies
├── PROJECT_PLAN.md       # Detailed project plan
├── BONUS_SQL_QUERY.md    # SQL query documentation
└── README.md             # This file
```

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Git

### 1. Clone and Setup

```bash
# Clone the repository
git clone <repository-url>
cd djagno-assessment

# Create .env file from example
make setup-env

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

### 2. Access the Application

- **API Root**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **Rides Endpoint**: http://localhost:8000/api/rides/
- **Users Endpoint**: http://localhost:8000/api/users/
- **Ride Events Endpoint**: http://localhost:8000/api/ride-events/

## 📚 API Documentation

### Authentication

All API endpoints require authentication. Use Django session authentication by logging in via the admin panel or DRF browsable API.

Only users with `role='admin'` in the User model (or Django superusers) can access the API.

### Endpoints

#### List Rides
```
GET /api/rides/
```

**Query Parameters:**
- `page`: Page number for pagination (default: 1)
- `status`: Filter by ride status (`en-route`, `pickup`, `dropoff`)
- `rider_email`: Filter by rider email (case-insensitive contains)
- `ordering`: Sort by `pickup_time` (use `-pickup_time` for descending)
- `latitude` & `longitude`: Sort by distance from GPS coordinates

**Example Requests:**
```bash
# Get all rides (paginated)
GET /api/rides/

# Filter by status
GET /api/rides/?status=pickup

# Filter by rider email
GET /api/rides/?rider_email=rider0@example.com

# Sort by distance from location
GET /api/rides/?latitude=37.75&longitude=-122.45

# Combine filters and pagination
GET /api/rides/?status=dropoff&page=2
```

**Response Format:**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/rides/?page=2",
  "previous": null,
  "results": [
    {
      "id_ride": 1,
      "status": "pickup",
      "rider": {
        "id_user": 1,
        "role": "rider",
        "first_name": "John",
        "last_name": "Doe",
        "email": "rider0@example.com",
        "phone_number": "+15550001"
      },
      "driver": {
        "id_user": 11,
        "role": "driver",
        "first_name": "Jane",
        "last_name": "Smith",
        "email": "driver0@example.com",
        "phone_number": "+16660001"
      },
      "pickup_latitude": 37.7749,
      "pickup_longitude": -122.4194,
      "dropoff_latitude": 37.7849,
      "dropoff_longitude": -122.4094,
      "pickup_time": "2025-11-10T10:30:00Z",
      "todays_ride_events": [
        {
          "id_ride_event": 1,
          "id_ride": 1,
          "description": "Status changed to pickup",
          "created_at": "2025-11-10T10:35:00Z"
        }
      ]
    }
  ]
}
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

## ⚡ Performance Optimization

### Query Optimization Strategy

The Ride List API achieves the **2-3 query target** through:

1. **select_related()** for ForeignKey relationships (rider, driver)
2. **prefetch_related()** with custom Prefetch for reverse FK (ride_events)
3. **Filtered prefetch** to only fetch events from last 24 hours

### Query Breakdown (verified with Django Debug Toolbar)

```
Query 1: Pagination count
Query 2: Main query with JOINs for rider and driver
Query 3: Prefetch query for today's ride events
```

**Example from Debug Toolbar:**
```sql
-- Query 1: Count
SELECT COUNT(*) FROM "ride"

-- Query 2: Rides with joined users
SELECT ... FROM "ride"
INNER JOIN "user" ON ("ride"."id_rider" = "user"."id_user")
INNER JOIN "user" T3 ON ("ride"."id_driver" = T3."id_user")
ORDER BY "ride"."pickup_time" DESC LIMIT 10

-- Query 3: Today's events
SELECT ... FROM "ride_event"
WHERE ("ride_event"."created_at" >= '2025-11-09T23:29:14.312192+00:00'
AND "ride_event"."id_ride" IN (13, 17, 57, 45, 43, 11, 21, 38, 68, 73))
```

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

## 📊 Bonus SQL Query - Trips Over 1 Hour

The bonus SQL query reports trips that took more than 1 hour from pickup to dropoff, grouped by month and driver.

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

### Sample Output

```
   month   |  driver   | count_of_trips_gt_1hr
-----------+-----------+-----------------------
 2025-10   | Driver0 U |                     3
 2025-10   | Driver1 U |                     4
 2025-10   | Driver2 U |                     7
 2025-10   | Driver3 U |                     5
 2025-11   | Driver0 U |                     2
 2025-11   | Driver1 U |                     3
```

### Query Explanation

1. **CTE (ride_durations)**: Uses conditional aggregation to find pickup and dropoff event times for each ride
2. **Duration Calculation**: `EXTRACT(EPOCH FROM (dropoff_time - pickup_time)) / 3600` converts time difference to hours
3. **Filtering**: `WHERE ... > 1` filters for trips longer than 1 hour
4. **Grouping**: Groups results by month (YYYY-MM format) and driver name

See [BONUS_SQL_QUERY.md](BONUS_SQL_QUERY.md) for detailed documentation.

## 🔧 Development Commands

All common commands are available via the Makefile:

```bash
# Container Management
make build              # Build Docker containers
make start              # Start containers (foreground)
make start-bg           # Start containers (background)
make stop               # Stop containers
make restart            # Restart containers
make logs               # View container logs

# Database
make migrations         # Create migrations
make migrate            # Run migrations
make dbshell            # Open PostgreSQL shell

# Django
make shell              # Open Django shell
make createsuperuser    # Create superuser
make manage ARGS='...'  # Run any manage.py command

# Data
make manage ARGS='generate_sample_data'                    # Generate 100 rides
make manage ARGS='generate_sample_data --rides=50'         # Generate 50 rides
make manage ARGS='flush --no-input'                        # Clear all data

# Utilities
make ssh                # SSH into web container
make help               # Show all available commands
```

## 🗂️ Database Schema

### User Table
| Field | Type | Description |
|-------|------|-------------|
| id_user | INT (PK) | Primary key |
| role | VARCHAR | User role (admin/rider/driver) |
| first_name | VARCHAR | First name |
| last_name | VARCHAR | Last name |
| email | VARCHAR | Email (unique) |
| phone_number | VARCHAR | Phone number |

### Ride Table
| Field | Type | Description |
|-------|------|-------------|
| id_ride | INT (PK) | Primary key |
| status | VARCHAR | Ride status (en-route/pickup/dropoff) |
| id_rider | INT (FK) | Foreign key to User |
| id_driver | INT (FK) | Foreign key to User |
| pickup_latitude | FLOAT | Pickup location latitude |
| pickup_longitude | FLOAT | Pickup location longitude |
| dropoff_latitude | FLOAT | Dropoff location latitude |
| dropoff_longitude | FLOAT | Dropoff location longitude |
| pickup_time | DATETIME | Scheduled pickup time |

### RideEvent Table
| Field | Type | Description |
|-------|------|-------------|
| id_ride_event | INT (PK) | Primary key |
| id_ride | INT (FK) | Foreign key to Ride |
| description | VARCHAR | Event description |
| created_at | DATETIME | Event timestamp |

## 🧪 Testing

### Manual Testing with DRF Browsable API

1. Login to admin: http://localhost:8000/admin/
2. Navigate to API: http://localhost:8000/api/rides/
3. Test filtering, sorting, and pagination using the UI

### Verify Query Performance

1. Visit: http://localhost:8000/api/rides/
2. Check Django Debug Toolbar (right sidebar)
3. Click "SQL" tab to see query count and details

## 🏗️ Design Decisions

### 1. Custom User Model
- Created a separate User model instead of extending Django's built-in User
- Follows the assessment requirements exactly
- Allows role-based permissions (admin/rider/driver)

### 2. Database Indexes
- Added indexes on frequently queried fields (email, status, created_at)
- Composite index on (pickup_latitude, pickup_longitude) for GPS sorting
- Improves query performance for large datasets

### 3. GPS Distance Sorting
- Implemented using Haversine formula with PostgreSQL functions
- Calculates distance at database level (not in Python)
- Maintains efficiency with large datasets

### 4. Serializer Strategy
- Separate serializers for list and detail views
- Optimized `RideListSerializer` for bulk queries
- Full `RideSerializer` for detail view with all relations

### 5. Docker-First Development
- Ensures consistency across development environments
- Easy setup for reviewers
- Production-ready containerization

## 🐛 Troubleshooting

### Debug Toolbar Not Showing
```python
# Settings already configured for Docker
# Toolbar should appear automatically when DEBUG=True
```

### Permission Denied Errors
```bash
# Make sure you're logged in as admin or superuser
# Check user role in admin panel
```

### Database Connection Issues
```bash
# Restart containers
make restart

# Check database is running
docker-compose ps
```

## 📝 Environment Variables

Create a `.env` file (copy from `.env.example`):

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_NAME=wingz_rides
DATABASE_USER=postgres
DATABASE_PASSWORD=postgres
DATABASE_HOST=db
DATABASE_PORT=5432
```

## 🚀 Deployment (Optional)

Ready for deployment to platforms like:
- Fly.io
- AWS ECS
- Heroku
- DigitalOcean App Platform

## 👨‍💻 Author

Built as part of the Wingz Django Engineer assessment.

## 📄 License

This project is for assessment purposes.
