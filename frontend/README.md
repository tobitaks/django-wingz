# Wingz Ride Management - Frontend

Vue.js 3 frontend application for the Wingz Ride Management API.

## Tech Stack

- **Framework**: Vue 3 (Composition API)
- **Build Tool**: Vite
- **Router**: Vue Router 4
- **State Management**: Pinia
- **HTTP Client**: Axios
- **CSS Framework**: Tailwind CSS
- **Icons**: Heroicons
- **Date/Time**: dayjs
- **Maps**: Leaflet

## Project Structure

```
src/
├── assets/           # Static assets and styles
├── components/       # Reusable components
│   ├── common/      # Generic components
│   ├── layout/      # Layout components
│   ├── rides/       # Ride-specific components
│   └── map/         # Map components
├── views/           # Page components
├── router/          # Vue Router configuration
├── stores/          # Pinia stores
├── services/        # API services
├── utils/           # Utility functions
├── composables/     # Composition functions
└── main.js          # Application entry point
```

## Setup

### Prerequisites
- Node.js 18+ and npm

### Installation

```bash
# Install dependencies
npm install

# Create environment file
cp .env.example .env.local

# Start development server
npm run dev
```

### Environment Variables

Create a `.env.local` file:

```
VITE_API_BASE_URL=http://localhost:8000/api
```

## Development

```bash
# Start dev server (http://localhost:5173)
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Current Progress

✅ **Phase 1: Project Setup** - COMPLETED
- Vue 3 + Vite initialized
- Core dependencies installed (router, pinia, axios)
- Tailwind CSS configured
- Additional dependencies (dayjs, leaflet, heroicons)
- Project structure created
- Environment configuration

⏳ **Phase 2: Core Components & Layout** - TODO
⏳ **Phase 3: API Integration** - TODO
⏳ **Phase 4: Ride List & Filtering** - TODO
⏳ **Phase 5: Map Integration** - TODO
⏳ **Phase 6: Authentication** - TODO
⏳ **Phase 7: Advanced Features** - TODO
⏳ **Phase 8: Polish & Optimization** - TODO

## Available Routes

- `/` - Redirects to `/rides`
- `/rides` - Ride list view (placeholder)

More routes will be added in subsequent phases.

## Backend Integration

Make sure the Django backend is running at http://localhost:8000 with CORS enabled:

```python
# Django settings.py
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # Vite dev server
]
```

## Next Steps

See [FRONTEND_PLAN.md](../FRONTEND_PLAN.md) in the project root for the complete development roadmap.

---

Built as part of the Wingz Django Engineer assessment.
