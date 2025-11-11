# Vue.js Frontend Plan - Wingz Ride Management

## Overview
Building a modern Vue.js 3 frontend to visualize and interact with the Wingz Ride Management API. Focus on clean UI/UX, real-time filtering, and interactive map features.

## 📊 Current Progress

✅ **Phase 1: Project Setup** - COMPLETED
✅ **Phase 2: Core Components & Layout** - COMPLETED
✅ **Phase 3: API Integration** - COMPLETED
✅ **Phase 4: Ride List & Filtering** - COMPLETED
⏳ **Phase 5: Map Integration** - TODO
✅ **Phase 6: Authentication** - COMPLETED
⏳ **Phase 7: Advanced Features** - TODO
⏳ **Phase 8: Polish & Optimization** - TODO

---

## Phase 1: Project Setup & Configuration ✅

### 1.1 Initialize Vue Project
- ✅ Create Vue 3 project with Vite
- ✅ Choose composition API or options API (using Composition API)
- ✅ Install core dependencies
  - vue-router (routing)
  - pinia (state management)
  - axios (HTTP client)
- ✅ Configure project structure
- ✅ Set up development environment

### 1.2 UI Framework Selection
- ✅ Selected Tailwind CSS (utility-first, lightweight)

### 1.3 Additional Dependencies
- ✅ Install date/time library (dayjs)
- ✅ Install map library (Leaflet)
- ✅ Install icons library (Heroicons)
- ✅ Set up environment variables (.env.example, .env.local)

### 1.4 Development Tools
- ✅ Git ignore configured (node_modules, dist, .env.local)
- ❌ ESLint configuration (optional - skipped)
- ❌ Prettier configuration (optional - skipped)

**Commit**: ✅ Initialize Vue.js frontend with Vite and Tailwind CSS

---

## Phase 2: Core Components & Layout ✅

### 2.1 Project Structure
```
frontend/
├── src/
│   ├── assets/           # Static assets
│   ├── components/       # Reusable components
│   │   ├── common/      # Generic components (Button, Card, etc.)
│   │   ├── rides/       # Ride-specific components
│   │   └── layout/      # Layout components
│   ├── views/           # Page components
│   ├── router/          # Vue Router config
│   ├── stores/          # Pinia stores
│   ├── services/        # API services
│   ├── utils/           # Utility functions
│   ├── composables/     # Reusable composition functions
│   └── App.vue
├── public/
└── package.json
```

### 2.2 Layout Components
- ✅ Create `AppHeader.vue` (navigation, user info, logout)
- ✅ Create `AppSidebar.vue` (filters, navigation)
- ❌ Create `AppFooter.vue` (skipped - not needed)
- ✅ Create `MainLayout.vue` (combine header, sidebar, content)
- ✅ Implement responsive design (mobile-first)

### 2.3 Common Components
- ✅ `LoadingSpinner.vue` - Loading indicator
- ✅ `ErrorAlert.vue` - Error message display
- ✅ `EmptyState.vue` - No data placeholder
- ✅ `Badge.vue` - Status badges
- ✅ `Pagination.vue` - Pagination controls

**Commit**: ✅ Add core layout and common components

---

## Phase 3: API Integration ✅

### 3.1 API Service Layer
- ✅ Create `src/services/api.js` - Axios instance with base config and CSRF handling
- ✅ Create `src/services/rideService.js` - Ride CRUD operations
- ✅ Create `src/services/userService.js` - User operations
- ✅ Create `src/services/authService.js` - Authentication with CSRF token
- ✅ Configure CORS in Django backend
- ✅ Set up API error handling

**API Service Structure:**
```javascript
// src/services/api.js
- axios instance with baseURL
- request interceptors (auth token)
- response interceptors (error handling)

// src/services/rideService.js
- getRides(params) - with filters, sorting, pagination
- getRideById(id)
- createRide(data)
- updateRide(id, data)
- deleteRide(id)
```

### 3.2 State Management
- ✅ Create `src/stores/rideStore.js` - Ride state
  - rides list
  - current ride
  - filters (status, rider_email)
  - sorting (pickup_time, distance)
  - pagination (page, total)
- ✅ Create `src/stores/authStore.js` - Authentication state
  - user info
  - isAuthenticated
  - login/logout methods
- ✅ Create `src/stores/uiStore.js` - UI state
  - loading states
  - error messages
  - sidebar open/closed

**Commit**: ✅ Implement API services and Pinia stores (combined with Phase 4 & 6)

---

## Phase 4: Ride List & Filtering ✅

### 4.1 Ride List View
- ✅ Create `views/RideListView.vue` - Main ride list page
- ✅ Create `components/rides/RideCard.vue` - Individual ride card
- ❌ Create `components/rides/RideTable.vue` - Table view (skipped - used cards)
- ✅ Display ride data:
  - Ride ID, status badge
  - Rider name, email
  - Driver name
  - Pickup/dropoff locations (coordinates)
  - Pickup time (formatted with dayjs)
  - Today's events count/badge
- ✅ Implement loading states
- ✅ Implement error handling
- ✅ Implement empty state

### 4.2 Filter Controls
- ✅ Create `components/rides/RideFilters.vue`
- ✅ Status filter dropdown (en-route, pickup, dropoff, all)
- ✅ Rider email search input (debounced)
- ✅ Clear filters button
- ❌ Filter state persisted in URL query params (skipped)
- ✅ Real-time filter application

### 4.3 Sorting Controls
- ✅ Pickup time sort (newest/oldest first)
- ❌ Distance sort (skipped - requires GPS input from Phase 5)
- ❌ Sort indicator icons (skipped)
- ❌ Sort state persisted in URL (skipped)

### 4.4 Pagination
- ✅ Display current page, total pages, total items
- ✅ Previous/Next buttons
- ✅ Page number display
- ❌ Jump to page input (skipped)
- ❌ Items per page selector (skipped - fixed at 10)

**Commit**: ✅ Implement ride list view with filtering and pagination (combined with Phase 3 & 6)

---

## Phase 5: Map Integration

### 5.1 Map Library Setup
**Recommendation**: Leaflet (free, no API key required for basic maps)

- [ ] Install Leaflet (`npm install leaflet vue-leaflet`)
- [ ] Import Leaflet CSS
- [ ] Create map component wrapper

### 5.2 Map View Components
- [ ] Create `components/map/RideMap.vue` - Main map component
- [ ] Display all rides as markers on map
- [ ] Color-code markers by status:
  - en-route: blue
  - pickup: yellow
  - dropoff: green
- [ ] Show pickup and dropoff locations for each ride
- [ ] Marker clustering for many rides
- [ ] Map bounds auto-adjust to show all markers

### 5.3 Interactive Map Features
- [ ] Click marker to show ride details popup
- [ ] Draw line between pickup and dropoff
- [ ] Current location button (get user's GPS)
- [ ] Distance sorting: click map to set reference point
- [ ] Filter rides by visible map area (optional)

### 5.4 Map + List Integration
- [ ] Create `views/RideMapView.vue` - Map-focused page
- [ ] Toggle between list view and map view
- [ ] Split view: map on left, list on right
- [ ] Hover on list item highlights marker
- [ ] Click marker filters list to that ride

**Commit**: Add interactive map with ride markers and GPS features

---

## Phase 6: Authentication ✅

### 6.1 Login Page
- ✅ Create `views/LoginView.vue`
- ✅ Login form (username, password)
- ✅ Form validation
- ✅ Error messages
- ❌ Remember me checkbox (skipped - not needed for session auth)
- ✅ Loading state during login

### 6.2 Authentication Flow
- ✅ Implement Django session authentication with CSRF protection
- ✅ Store auth state in Pinia
- ✅ Protected routes (require auth)
- ✅ Redirect to login if not authenticated
- ✅ Redirect to rides after login
- ✅ Logout functionality

### 6.3 User Interface
- ✅ Display logged-in user info in header
- ✅ Logout button in header
- ✅ Display user initial avatar
- ❌ Session timeout handling (not implemented)

### 6.4 Backend Authentication Endpoints
- ✅ Created `/api/auth/csrf/` - Get CSRF token
- ✅ Created `/api/auth/login/` - Session login
- ✅ Created `/api/auth/logout/` - Session logout
- ✅ Created `/api/auth/check/` - Check auth status
- ✅ Configured CSRF_TRUSTED_ORIGINS in Django

**Commit**: ✅ Implement authentication with login page and protected routes (combined with Phase 3 & 4)

---

## Phase 7: Advanced Features

### 7.1 Ride Detail Page
- [ ] Create `views/RideDetailView.vue`
- [ ] Display full ride information
- [ ] Show rider and driver details
- [ ] Display all ride events (not just today's)
- [ ] Show pickup/dropoff on mini map
- [ ] Calculate estimated distance/duration
- [ ] Edit ride button (opens modal)
- [ ] Delete ride button (with confirmation)

### 7.2 Create/Edit Ride
- [ ] Create `components/rides/RideFormModal.vue`
- [ ] Form fields for all ride data
- [ ] Rider/driver selection (searchable dropdown)
- [ ] GPS coordinate input or map click
- [ ] Date/time picker for pickup time
- [ ] Form validation
- [ ] Submit to API
- [ ] Success/error feedback

### 7.3 Ride Events Timeline
- [ ] Create `components/rides/RideEventsTimeline.vue`
- [ ] Display events in chronological order
- [ ] Visual timeline with icons
- [ ] Timestamp formatting
- [ ] Today's events highlighted
- [ ] Add new event functionality (optional)

### 7.4 Real-time Updates (Optional)
- [ ] WebSocket connection to Django Channels
- [ ] Auto-refresh ride list on updates
- [ ] Toast notifications for new rides/events
- [ ] Live status updates

### 7.5 Dashboard/Statistics (Optional)
- [ ] Create `views/DashboardView.vue`
- [ ] Ride statistics cards:
  - Total rides
  - Active rides (en-route, pickup)
  - Completed rides (dropoff)
  - Rides by status chart
- [ ] Recent activity feed
- [ ] Top drivers/riders

**Commit**: Add ride detail page, create/edit forms, and events timeline

---

## Phase 8: Polish & Optimization

### 8.1 UI/UX Improvements
- [ ] Smooth transitions and animations
- [ ] Loading skeletons instead of spinners
- [ ] Toast notifications for actions
- [ ] Keyboard shortcuts (Ctrl+F for filter, etc.)
- [ ] Dark mode toggle (optional)
- [ ] Responsive design for mobile/tablet
- [ ] Touch gestures for mobile map

### 8.2 Performance Optimization
- [ ] Lazy load routes (code splitting)
- [ ] Debounce search inputs
- [ ] Virtualize long lists (virtual scrolling)
- [ ] Cache API responses
- [ ] Optimize bundle size
- [ ] Lazy load map library
- [ ] Image optimization

### 8.3 Error Handling & Validation
- [ ] Global error handler
- [ ] Network error messages
- [ ] Form validation with helpful messages
- [ ] 404 page for invalid routes
- [ ] API error display improvements

### 8.4 Testing (Optional but Recommended)
- [ ] Unit tests for utilities/composables
- [ ] Component tests with Vitest
- [ ] E2E tests with Playwright/Cypress
- [ ] API mock for testing

### 8.5 Documentation
- [ ] Update main README with frontend setup
- [ ] Create FRONTEND.md with architecture details
- [ ] Component documentation
- [ ] API service documentation
- [ ] Development guide

**Commit**: Polish UI/UX, optimize performance, and add documentation

---

## Technology Stack

### Core
- **Framework**: Vue 3 (Composition API)
- **Build Tool**: Vite
- **Router**: Vue Router 4
- **State Management**: Pinia
- **HTTP Client**: Axios

### UI/Styling
- **CSS Framework**: Tailwind CSS (recommended)
- **Icons**: Heroicons or FontAwesome
- **Date/Time**: dayjs

### Map
- **Map Library**: Leaflet + vue-leaflet
- **Tile Provider**: OpenStreetMap (free)

### Development
- **Linting**: ESLint
- **Formatting**: Prettier
- **Testing**: Vitest + Playwright (optional)

---

## Project Structure (Final)

```
frontend/
├── public/
│   └── favicon.ico
├── src/
│   ├── assets/
│   │   ├── styles/
│   │   │   └── main.css          # Tailwind imports
│   │   └── images/
│   ├── components/
│   │   ├── common/
│   │   │   ├── LoadingSpinner.vue
│   │   │   ├── ErrorAlert.vue
│   │   │   ├── EmptyState.vue
│   │   │   ├── Badge.vue
│   │   │   └── Pagination.vue
│   │   ├── layout/
│   │   │   ├── AppHeader.vue
│   │   │   ├── AppSidebar.vue
│   │   │   └── MainLayout.vue
│   │   ├── rides/
│   │   │   ├── RideCard.vue
│   │   │   ├── RideTable.vue
│   │   │   ├── RideFilters.vue
│   │   │   ├── RideFormModal.vue
│   │   │   └── RideEventsTimeline.vue
│   │   └── map/
│   │       └── RideMap.vue
│   ├── views/
│   │   ├── LoginView.vue
│   │   ├── RideListView.vue
│   │   ├── RideDetailView.vue
│   │   ├── RideMapView.vue
│   │   └── DashboardView.vue (optional)
│   ├── router/
│   │   └── index.js
│   ├── stores/
│   │   ├── rideStore.js
│   │   ├── authStore.js
│   │   └── uiStore.js
│   ├── services/
│   │   ├── api.js
│   │   ├── rideService.js
│   │   ├── userService.js
│   │   └── authService.js
│   ├── utils/
│   │   ├── formatters.js        # Date, currency, etc.
│   │   ├── validators.js        # Form validation
│   │   └── constants.js         # App constants
│   ├── composables/
│   │   ├── useRides.js          # Ride data fetching
│   │   ├── useFilters.js        # Filter logic
│   │   └── useGeolocation.js    # GPS utilities
│   ├── App.vue
│   └── main.js
├── .env.example
├── .env.local
├── .eslintrc.js
├── .prettierrc
├── index.html
├── package.json
├── tailwind.config.js
├── vite.config.js
└── README.md
```

---

## Git Commit Strategy

### Recommended Commits:
1. **Initial setup**: "Initialize Vue.js project with Vite and Tailwind"
2. **Layout**: "Add core layout and common components"
3. **API**: "Implement API services and Pinia stores"
4. **Ride list**: "Add ride list view with filtering and pagination"
5. **Map**: "Integrate Leaflet map with ride markers"
6. **Auth**: "Implement authentication with login page"
7. **Detail/Forms**: "Add ride detail page and create/edit forms"
8. **Polish**: "Polish UI/UX and optimize performance"

---

## Development Timeline Estimate

- **Phase 1**: 1-2 hours (setup)
- **Phase 2**: 2-3 hours (layout & components)
- **Phase 3**: 2-3 hours (API integration)
- **Phase 4**: 3-4 hours (ride list & filtering)
- **Phase 5**: 3-4 hours (map integration)
- **Phase 6**: 2-3 hours (authentication)
- **Phase 7**: 4-5 hours (advanced features)
- **Phase 8**: 2-3 hours (polish)

**Total Estimate: 19-27 hours** (2-3 days of focused work)

---

## Success Criteria

- [ ] All rides displayed with proper data
- [ ] Filtering by status and rider email works
- [ ] Sorting by pickup time works
- [ ] GPS-based distance sorting works
- [ ] Pagination works correctly
- [ ] Map shows all rides with markers
- [ ] Authentication flow works
- [ ] Can create/edit/delete rides
- [ ] Responsive design (mobile-friendly)
- [ ] Clean, professional UI
- [ ] Good performance (fast load, smooth interactions)
- [ ] Error handling implemented
- [ ] Code is well-organized and documented

---

## Nice-to-Have Features

### Low Priority
- [ ] Dark mode
- [ ] Export rides to CSV/Excel
- [ ] Print ride details
- [ ] Ride search by ID
- [ ] Bulk actions (delete multiple)
- [ ] Ride assignment workflow
- [ ] Driver/rider profiles

### Future Enhancements
- [ ] Real-time updates with WebSocket
- [ ] Mobile app (React Native or Capacitor)
- [ ] Advanced analytics dashboard
- [ ] Route optimization suggestions
- [ ] Integration with mapping APIs (Google Maps, Mapbox)
- [ ] SMS/Email notifications
- [ ] Multi-language support (i18n)

---

## Notes

### CORS Configuration in Django
Make sure Django backend has CORS enabled for the frontend:

```python
# config/settings.py
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # Vite default port
    'http://localhost:3000',  # Alternative port
]
```

### API Base URL
Frontend `.env.local`:
```
VITE_API_BASE_URL=http://localhost:8000/api
```

### Authentication Strategy
- Use Django session authentication (cookies)
- Or implement Token authentication
- Store auth state in Pinia store
- Persist in localStorage (optional)

---

## Ready to Start?

**Recommended Starting Point**: Phase 1
**First Commit**: Initialize Vue.js project with Vite and Tailwind CSS
**First Goal**: Get basic ride list displaying from API

Good luck building the frontend! 🚀
