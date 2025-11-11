# Wingz Ride Management System

A full-stack ride-sharing management application with Django REST Framework backend and Vue.js frontend, featuring performance-optimized APIs and a modern, responsive user interface.

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

### Frontend (Vue.js 3)
- **Modern UI**: Built with Vue 3 Composition API and Tailwind CSS
- **Ride Management**: Complete CRUD operations for rides
- **Advanced Filtering**: Filter rides by status and rider email
- **Sorting & Pagination**: Sort by pickup time with paginated results
- **Responsive Design**: Works seamlessly on desktop and mobile
- **Real-time Validation**: Form validation with error feedback
- **Session Management**: Secure login/logout with route guards

## Tech Stack

### Backend
- Python 3.10
- Django 5.0
- Django REST Framework 3.14
- PostgreSQL 15

### Frontend
- Vue.js 3 (Composition API)
- Vite 7
- Vue Router 4
- Pinia (State Management)
- Tailwind CSS 3
- Axios
- Heroicons

### Development Tools
- Docker & Docker Compose
- Django Debug Toolbar
- Makefile for common commands

## Project Structure

```
djagno-assessment/
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
├── frontend/              # Vue.js application
│   ├── src/
│   │   ├── components/    # Vue components
│   │   │   ├── common/    # Reusable components
│   │   │   ├── layout/    # Layout components
│   │   │   └── rides/     # Ride-specific components
│   │   ├── views/         # Page components
│   │   ├── stores/        # Pinia stores
│   │   ├── services/      # API service layer
│   │   ├── router/        # Vue Router configuration
│   │   └── assets/        # Static assets
│   ├── package.json
│   └── vite.config.js
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
cd djagno-assessment

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

### Manual Setup

```bash
# Build and start containers
make build
make start-bg

# Run migrations
make migrate

# Create superuser for admin access
make createsuperuser

# Generate sample data
make generate-data
```

### Start Frontend Development Server

```bash
cd frontend
npm install
npm run dev
```

### Access the Application

- **Frontend**: http://localhost:5173/
- **API Root**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/
- **API Rides Endpoint**: http://localhost:8000/api/rides/

### Default Credentials

After running `make generate-data`, you can login with:
- **Email**: admin@wingz.com
- **Password**: (set during `make createsuperuser`)

## API Documentation

### Authentication

The API uses session-based authentication with CSRF protection.

**Login:**
```bash
POST /api/auth/login/
Content-Type: application/json

{
  "username": "admin@wingz.com",
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

#### Users

- `GET /api/users/` - List all users (no pagination)
- `POST /api/users/` - Create user
- `GET /api/users/{id}/` - Get user detail
- `PUT/PATCH /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user

#### Ride Events

- `GET /api/ride-events/` - List ride events
- `POST /api/ride-events/` - Create ride event
- `GET /api/ride-events/{id}/` - Get event detail
- `PUT/PATCH /api/ride-events/{id}/` - Update event
- `DELETE /api/ride-events/{id}/` - Delete event

## Frontend Features

### Pages

1. **Login Page** (`/login`)
   - Session-based authentication
   - Form validation and error handling
   - Automatic redirect to rides list after login

2. **Rides List** (`/rides`)
   - View all rides in a card grid layout
   - Filter by status and rider email
   - Sort by pickup time (ascending/descending)
   - Pagination controls
   - Create new ride button
   - Click card to view details

3. **Ride Detail** (`/rides/:id`)
   - View full ride information
   - Rider and driver details
   - Edit ride with pre-filled form
   - Delete ride with confirmation

### Components

**Common Components:**
- `Badge` - Status badges with color variants
- `LoadingSpinner` - Loading indicators
- `ErrorAlert` - Error messages with dismiss
- `EmptyState` - Empty state placeholders
- `Pagination` - Pagination controls

**Ride Components:**
- `RideCard` - Individual ride card display
- `RideFilters` - Status and email filters
- `RideFormModal` - Create/edit ride modal form

**Layout Components:**
- `AppHeader` - Application header with user info and logout
- `MainLayout` - Main page layout wrapper

### State Management

The application uses Pinia stores for state management:

- **authStore**: User authentication state
- **rideStore**: Rides data, filters, pagination
- **uiStore**: UI state (modals, notifications)

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

## Development Commands

### Container Management
```bash
make build              # Build Docker containers
make start              # Start containers (foreground)
make start-bg           # Start containers (background)
make stop               # Stop containers
make restart            # Restart containers
make logs               # View container logs
make ps                 # Show running containers
```

### Database
```bash
make migrate            # Run migrations
make migrations         # Create new migrations
make dbshell            # Open PostgreSQL shell
make showmigrations     # Show migration status
```

### Django
```bash
make shell              # Open Django shell
make createsuperuser    # Create superuser
make manage ARGS='...'  # Run any manage.py command
make check              # Run Django system checks
make collectstatic      # Collect static files
```

### Data Management
```bash
make generate-data                              # Generate sample data (default: 100 rides)
make manage ARGS='generate_sample_data --rides=50'   # Generate 50 rides
make manage ARGS='flush --no-input'                  # Clear all data
```

### Testing
```bash
make test               # Run all tests
make test ARGS='rides'  # Run specific app tests
```

### Cleanup
```bash
make clean              # Remove containers and volumes
make rebuild            # Clean rebuild (down, build, start, migrate)
```

### Frontend Development
```bash
cd frontend
npm install             # Install dependencies
npm run dev             # Start dev server
npm run build           # Build for production
npm run preview         # Preview production build
```

## Requirements Met

### Backend
✅ Django REST Framework with ViewSets
✅ Models: User, Ride, RideEvent
✅ Serializers with nested relations
✅ Session-based authentication with CSRF protection
✅ Filtering (status, rider email)
✅ Sorting (pickup_time, GPS distance)
✅ Pagination support
✅ Performance optimization (2-3 queries)
✅ `todays_ride_events` field (last 24 hours only)
✅ Bonus SQL query for trips > 1 hour

### Frontend
✅ Vue.js 3 with Composition API
✅ Complete CRUD operations for rides
✅ Authentication with login/logout
✅ Filtering and sorting UI
✅ Pagination controls
✅ Form validation
✅ Responsive design
✅ Error handling and loading states

---

Built as part of the Wingz Django Engineer assessment.
