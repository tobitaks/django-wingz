from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RideViewSet, RideEventViewSet
from .auth_views import login_view, logout_view, current_user_view, check_auth_view, csrf_view

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'rides', RideViewSet, basename='ride')
router.register(r'ride-events', RideEventViewSet, basename='rideevent')

urlpatterns = [
    path('', include(router.urls)),
    # Authentication endpoints
    path('auth/csrf/', csrf_view, name='auth-csrf'),
    path('auth/login/', login_view, name='auth-login'),
    path('auth/logout/', logout_view, name='auth-logout'),
    path('auth/user/', current_user_view, name='auth-current-user'),
    path('auth/check/', check_auth_view, name='auth-check'),
]
