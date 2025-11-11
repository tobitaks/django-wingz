# Wingz Django Assessment - Project Plan

## Overview
Building a RESTful API using Django REST Framework for managing ride information with focus on performance optimization.

## 📊 Current Progress

⏳ **Phase 1: Project Setup & Core Models** - IN PROGRESS
⏳ **Phase 2: API Foundation** - TODO
⏳ **Phase 3: Performance Optimization** - TODO
⏳ **Phase 4: Advanced Features** - TODO
⏳ **Phase 5: Bonus SQL Query** - TODO
⏳ **Phase 6: Vue.js Frontend** - TODO (Optional)
⏳ **Phase 7: Deployment** - TODO (Optional)
⏳ **Phase 8: Final Polish** - TODO

### Development Approach:
Building the project with clean, incremental git commits showing logical progression. Each phase will be implemented step-by-step with meaningful commit messages.

### Next Steps:
1. Set up project structure with Docker
2. Create database models with proper indexes
3. Implement serializers with nested relations
4. Build ViewSets with performance optimization (2-3 queries)
5. Add filtering, sorting, and pagination
6. Write bonus SQL query
7. Create comprehensive documentation
8. (Optional) Add Vue.js frontend
9. (Optional) Deploy to Fly.io

---

## Phase 1: Project Setup & Core Models

### 1.1 Environment Setup
- [ ] Create virtual environment
- [ ] Install Django, DRF, PostgreSQL dependencies
- [ ] Initialize Django project structure
- [ ] Configure settings for development

### 1.2 Database Configuration
- [ ] Set up PostgreSQL database (via Docker)
- [ ] Configure database settings
- [ ] Environment variables for database config
- [ ] Add PostGIS extension (for GPS distance calculations - optional)

### 1.3 Model Creation
- [ ] Create User model
  - id_user (PK)
  - role (admin/rider/driver)
  - first_name, last_name, email, phone_number
- [ ] Create Ride model
  - id_ride (PK)
  - status (en-route/pickup/dropoff)
  - id_rider, id_driver (FKs to User)
  - pickup_latitude, pickup_longitude
  - dropoff_latitude, dropoff_longitude
  - pickup_time
  - Database indexes for performance
- [ ] Create RideEvent model
  - id_ride_event (PK)
  - id_ride (FK to Ride)
  - description
  - created_at
  - Database indexes for performance
- [ ] Run initial migrations
- [ ] Register models in admin
- [ ] Create sample data generator command

---

## Phase 2: API Foundation

### 2.1 Serializers
- [ ] UserSerializer (basic fields)
- [ ] RideEventSerializer
- [ ] RideSerializer (with nested relations)
  - Include rider and driver details
  - Include ride events
  - Add todays_ride_events field
- [ ] RideListSerializer (optimized for list view)

### 2.2 ViewSets
- [ ] UserViewSet with basic CRUD
- [ ] RideViewSet with optimized queries
- [ ] RideEventViewSet with basic CRUD
- [ ] Configure URL routing
- [ ] Test with DRF browsable API

### 2.3 Authentication
- [ ] Implement admin-only permission class (IsAdminUser)
- [ ] Configure DRF authentication settings
- [ ] Test authentication flow

---

## Phase 3: Performance Optimization ⚡ (CRITICAL)

### 3.1 Query Optimization
- [ ] Implement select_related() for rider and driver FKs
- [ ] Implement prefetch_related() for ride_events
- [ ] Custom Prefetch for todays_ride_events (last 24h only)
- [ ] Verify 2-3 query target achieved (need to test with Debug Toolbar)

### 3.2 Testing & Verification
- [ ] Add Django Debug Toolbar for query analysis
- [ ] Create test data generator (generate_sample_data command)
- [ ] Measure and document query count
- [ ] Profile performance with large dataset

---

## Phase 4: Advanced Features

### 4.1 Filtering
- [ ] Add filter by ride status
- [ ] Add filter by rider email
- [ ] Use django-filter with RideFilter class
- [ ] Test filter combinations with sample data

### 4.2 Sorting
- [ ] Implement sorting by pickup_time
- [ ] Implement GPS-based distance sorting
  - Accept lat/lng as query parameters
  - Use Haversine formula with database functions
  - Maintain efficient database-level sorting
- [ ] Ensure sorting works with pagination

### 4.3 Pagination
- [ ] Configure DRF pagination (PageNumberPagination)
- [ ] Test with large datasets
- [ ] Verify query optimization maintained

### 4.4 Error Handling
- [ ] Add basic input validation (serializers)
- [ ] Handle edge cases (missing GPS coords handled gracefully)
- [ ] Return appropriate HTTP status codes (DRF default)
- [ ] Add custom error messages

---

## Phase 5: Bonus SQL Query

### 5.1 Raw SQL Report
- [ ] Write SQL query for trips >1 hour
  - Join Ride, RideEvent, User tables
  - Find pickup and dropoff events
  - Calculate time difference
  - Filter for >1 hour duration
  - Group by month and driver
- [ ] Test query with sample data
- [ ] Document query in README

---

## Phase 6: Vue.js Frontend (Bonus)

### 6.1 Vue Setup
- [ ] Initialize Vue 3 project (Vite)
- [ ] Configure API client (axios)
- [ ] Set up CORS in Django

### 6.2 Core UI Components
- [ ] Ride list table/cards
- [ ] Pagination controls
- [ ] Filter controls (status, email)
- [ ] Sort controls (time, distance)
- [ ] Authentication/login form

### 6.3 Enhanced Features (Optional)
- [ ] Map view with Leaflet/Mapbox
- [ ] GPS location picker for distance sorting
- [ ] Ride details modal
- [ ] Today's events badge/indicator

---

## Phase 7: Deployment

### 7.1 Docker Setup
- [ ] Create Dockerfile for Django
- [ ] Create docker-compose.yml (Django + PostgreSQL)
- [ ] Configure static files
- [ ] Test local Docker build

### 7.2 Fly.io Deployment
- [ ] Install flyctl CLI
- [ ] Create fly.toml configuration
- [ ] Set up PostgreSQL on Fly.io
- [ ] Configure environment variables
- [ ] Deploy application
- [ ] Run migrations on production
- [ ] Test live deployment

### 7.3 Documentation
- [ ] Comprehensive README
  - Setup instructions
  - API documentation
  - Design decisions
  - Performance notes
  - Bonus SQL query
  - Live demo URL
- [ ] API endpoint examples
- [ ] Environment variables template

---

## Phase 8: Final Polish

### 8.1 Code Quality
- [ ] Code review and refactoring
- [ ] Add docstrings and comments
- [ ] Remove debug code
- [ ] Ensure PEP 8 compliance

### 8.2 Git History
- [ ] Clean, meaningful commits
- [ ] Clear progression of features
- [ ] Proper commit messages

### 8.3 Testing
- [ ] Create sample data fixtures
- [ ] Test all endpoints
- [ ] Test filter/sort combinations
- [ ] Verify performance targets

---

## Success Criteria

- ✅ All core requirements implemented
- ✅ 2-3 database queries for Ride List API
- ✅ todays_ride_events filtering works correctly
- ✅ Admin-only authentication working
- ✅ Filtering, sorting, pagination functional
- ✅ Bonus SQL query completed
- ✅ Clean, meaningful commit history
- ✅ Comprehensive README
- ✅ (Bonus) Vue.js frontend working
- ✅ (Bonus) Live deployment on Fly.io

---

## Notes & Design Decisions

### Performance Strategy
- Use select_related() for ForeignKey relationships (rider, driver)
- Use prefetch_related() with custom Prefetch for reverse FK (ride_events)
- Filter todays_ride_events in the Prefetch queryset using timezone-aware comparison

### GPS Distance Sorting
- Option 1: PostGIS ST_Distance with indexed geometry columns (best performance)
- Option 2: Database-level Haversine formula in raw SQL
- Option 3: Django ORM with custom database functions

### Authentication
- Using DRF's built-in authentication (TokenAuthentication or SessionAuthentication)
- Custom permission class: IsAdminUser based on User.role field

### Tech Stack
- Python 3.11+
- Django 5.0+
- Django REST Framework 3.14+
- PostgreSQL 15+ with PostGIS
- Vue.js 3 (frontend)
- Docker
- Fly.io (deployment)

---

## Timeline Estimate

- Phase 1-2: 2-3 hours
- Phase 3: 1-2 hours (critical optimization)
- Phase 4: 2-3 hours
- Phase 5: 1 hour
- Phase 6: 2-3 hours
- Phase 7: 1-2 hours
- Phase 8: 1 hour

**Total: ~10-15 hours**
