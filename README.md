# Wingz Ride Management System

A Django REST Framework backend for managing ride-sharing operations with performance-optimized APIs, featuring advanced filtering, GPS-based sorting, and comprehensive CRUD operations.

## 🚀 Live Demo

**Production URL**: <a href="https://django-wingz.fly.dev/" target="_blank">https://django-wingz.fly.dev/</a>

**Test Credentials:**
- Username: `admin`
- Password: `admin123`

**Quick Links:**
- <a href="https://django-wingz.fly.dev/" target="_blank">Frontend</a>
- <a href="https://django-wingz.fly.dev/api/" target="_blank">API Root</a>
- <a href="https://django-wingz.fly.dev/admin/" target="_blank">Admin Panel</a>

## Features

### Backend (Django REST Framework)
- **Full CRUD API** for Rides, Users, and Ride Events
- **Performance Optimized**: Achieves 2-3 database queries for ride list endpoint
- **Advanced Filtering**: Filter by ride status and rider email
- **Smart Sorting**: Sort by pickup time or GPS distance from any location
- **Pagination**: Built-in pagination for all list endpoints
- **Session-based Authentication**: Secure authentication with CSRF protection
- **Role-based Access Control**: Admin-only API access
- **Sample Data Generator**: Command to generate realistic test data

## Tech Stack

### Backend
- Python 3.10
- Django 5.0
- Django REST Framework 3.14
- PostgreSQL 15

### Development Tools
- Docker & Docker Compose
- Django Debug Toolbar
- Makefile for common commands

## Project Structure

```
django-wingz/
├── config/                 # Django project settings
│   ├── settings.py        # Main settings with REST Framework & CORS config
│   ├── urls.py            # Root URL configuration
│   └── wsgi.py
├── rides/                 # Main Django application
│   ├── models.py          # User, Ride, RideEvent models
│   ├── serializers.py     # DRF serializers with optimization
│   ├── views.py           # ViewSets with query optimization
│   ├── auth_views.py      # Authentication endpoints
│   ├── permissions.py     # IsAdminUser permission class
│   ├── filters.py         # Custom filter for rides
│   ├── urls.py            # API routes
│   └── management/
│       └── commands/
│           └── generate_sample_data.py
├── docker-compose.yml     # Docker services configuration
├── Dockerfile             # Django container definition
├── Makefile               # Common commands
└── requirements/          # Python dependencies
```

## Quick Start

### Prerequisites
- Docker and Docker Compose installed

### One-Command Setup

```bash
# Clone the repository
git clone https://github.com/tobitaks/django-wingz
cd django-wingz

# Initialize everything (build, migrate, create superuser, generate data)
make init
```

This will:
1. Create `.env` file from template
2. Build Docker containers
3. Start services in background
4. Run database migrations
5. Prompt to create a superuser
6. Generate sample data (users, rides, events)


### Access the Backend

- **API Root**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **API Rides Endpoint**: http://localhost:8000/api/rides/

#### Using the Django Admin Panel

The Django admin provides a full-featured interface for managing all data:

1. **Open your browser** and navigate to http://localhost:8000/admin/
2. **Login** with your superuser credentials (created during `make init`)
3. **Manage data**:
   - **Users**: Create/edit riders, drivers, and admin users
   - **Rides**: Create/edit rides with all fields
   - **Ride Events**: Create/edit ride events
   - **View relationships**: See linked riders, drivers, and events for each ride
   - **Bulk actions**: Delete multiple records at once
   - **Search & Filter**: Use the built-in search and filter options

#### Using the DRF Browsable API

Django REST Framework provides a web-based interface for exploring and interacting with the API:

1. **Access the browsable API** in the same browser (make sure that you're already logged in as admin):
   - **API Root**: http://localhost:8000/api/ - Shows all available endpoints
   - **Rides**: http://localhost:8000/api/rides/ - List/Create rides
   - **Ride Detail**: http://localhost:8000/api/rides/1/ - View/Update/Delete specific ride
   - **Users**: http://localhost:8000/api/users/ - List users
   - **Ride Events**: http://localhost:8000/api/ride-events/ - List events

2. **Perform operations**:
   - **GET**: Click on any endpoint to view data
   - **POST**: Use the form at the bottom of list views to create new records
   - **PUT/PATCH**: Use the form on detail views to update records
   - **DELETE**: Use the delete button on detail views
   - **Filter**: Add query parameters like `?status=pickup` or `?rider_email=test@example.com`
   - **Sort**: Add `?ordering=-pickup_time` to sort by pickup time (descending)

**Note:** Since the API uses session authentication, you must login through the admin panel first before accessing the browsable API.


## API Documentation

### Authentication

The API uses session-based authentication with CSRF protection.

**Login:**
```bash
POST /api/auth/login/
Content-Type: application/json

{
  "username": "your-username",
  "password": "your-password"
}
```

**Logout:**
```bash
POST /api/auth/logout/
```

**Check Authentication:**
```bash
GET /api/auth/check/
```

All ride management endpoints require authentication. Only users with `role='admin'` (or Django superusers) can access the API.

### Endpoints

#### Rides

**List Rides**
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

**Get Ride Detail**
```
GET /api/rides/{id}/
```

**Create Ride**
```
POST /api/rides/
Content-Type: application/json

{
  "status": "en-route",
  "id_rider_id": 3,
  "id_driver_id": 14,
  "pickup_latitude": 37.7749,
  "pickup_longitude": -122.4194,
  "dropoff_latitude": 37.7849,
  "dropoff_longitude": -122.4094,
  "pickup_time": "2025-11-10T10:30:00Z"
}
```

**Update Ride**
```
PUT /api/rides/{id}/
PATCH /api/rides/{id}/
```

**Delete Ride**
```
DELETE /api/rides/{id}/
```

## Performance Optimization

### Backend Query Optimization

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

    # prefetch_related() - Efficiently fetch today's ride events in a separate query
    # This prevents N+1 queries when accessing ride events
    todays_events_prefetch = Prefetch(
        'ride_events',
        queryset=RideEvent.objects.filter(created_at__gte=cutoff_time),
        to_attr='todays_ride_events_prefetch'
    )

    # select_related() - Performs SQL JOIN to fetch rider and driver in the same query
    # prefetch_related() - Applies the custom prefetch for ride events
    queryset = Ride.objects.select_related(
        'id_rider',   # JOIN with rider (ForeignKey)
        'id_driver'   # JOIN with driver (ForeignKey)
    ).prefetch_related(
        todays_events_prefetch  # Separate query for events
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

## Testing

The project includes comprehensive unit tests covering Ride models, serializers, API endpoints, filtering, sorting, authentication, and performance optimization.

### Test Coverage

**30 test cases covering:**
- **Ride Model Tests**: Ride creation, validation, relationships, and cascade deletion
- **RideEvent Model Tests**: Event creation, auto timestamps, and relationships
- **Ride Serializer Tests**: Field validation and nested relationships (rider/driver)
- **API Tests**: Full CRUD operations (Create, Read, Update, Delete)
- **Authentication Tests**: Login, logout, and session management
- **Filtering Tests**: Status and rider email filtering
- **Sorting Tests**: Pickup time and GPS distance sorting
- **Performance Tests**: Query optimization (2-3 queries) and event filtering

### Running Tests

```bash
# Run all tests
make test

# Run specific test class
make test ARGS="rides.tests.RideAPITest"

# Run specific test method
make test ARGS="rides.tests.RideAPITest.test_create_ride"

# Run with verbose output
make test ARGS="-v 2"
```

### Test Results

All 30 tests pass successfully:
- ✅ 5 Ride model tests
- ✅ 4 RideEvent model tests
- ✅ 2 Ride serializer tests
- ✅ 4 Authentication tests
- ✅ 7 Ride API CRUD tests
- ✅ 6 Filtering and sorting tests
- ✅ 2 Performance optimization tests

## Common Development Commands

```bash
# Setup
make init               # One-command setup (build, migrate, create superuser, generate data, start server)
make help               # Show all available commands

# Container management
make start              # Start containers and show logs
make stop               # Stop containers
make clean              # Remove containers and volumes

# Testing
make test               # Run all tests

# Database
make dbshell            # Open PostgreSQL shell (for running SQL queries)
```

---

## Bonus: Vue.js Frontend

A modern, responsive frontend interface built with Vue.js 3 has been included as a bonus feature for this project.

### Frontend Features
- **Modern UI**: Built with Vue 3 Composition API and Tailwind CSS
- **Ride Management**: View and interact with ride data
- **Advanced Filtering**: Filter rides by status and rider email
- **Sorting & Pagination**: Sort by pickup time with paginated results
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Real-time Validation**: Form validation with error feedback
- **Session Management**: Secure login/logout with route guards

### Frontend Tech Stack
- Vue.js 3 (Composition API)
- Vite 7
- Vue Router 4
- Pinia (State Management)
- Tailwind CSS 3
- Axios
- Heroicons

### Frontend Project Structure

```
frontend/              # Vue.js application
├── src/
│   ├── components/    # Vue components
│   │   ├── common/    # Reusable components
│   │   ├── layout/    # Layout components
│   │   └── rides/     # Ride-specific components
│   ├── views/         # Page components
│   ├── stores/        # Pinia stores
│   ├── services/      # API service layer
│   ├── router/        # Vue Router configuration
│   └── assets/        # Static assets
├── package.json
└── vite.config.js
```

### Frontend Setup

```bash
# In a second terminal tab, start the frontend development server
cd frontend
npm install
npm run dev
```

### Access the Frontend

- **Frontend**: http://localhost:5173/

### Production Deployment

The application is deployed on Fly.io with integrated frontend and backend:

- **Production URL**: https://django-wingz.fly.dev/

**Login Credentials (for testing):**
- **Username**: `admin`
- **Email**: `admin@wingz.com`
- **Password**: `admin123`

**Access Points:**
- **Frontend**: https://django-wingz.fly.dev/
- **API Root**: https://django-wingz.fly.dev/api/
- **Admin Panel**: https://django-wingz.fly.dev/admin/

The production build includes:
- Multi-stage Docker build (Vue.js build + Django)
- WhiteNoise for static file serving
- PostgreSQL database
- Production-ready security settings
- Sample data pre-loaded (21 users, 100 rides, 554 events)
