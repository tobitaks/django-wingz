"""
Production settings for Fly.io deployment
"""
import os
import dj_database_url
from .settings import *

# SECURITY
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')

# Allow build-time dummy secret key for collectstatic, but require real key at runtime
if not SECRET_KEY:
    # Check if we're just running collectstatic (build time)
    import sys
    if 'collectstatic' not in sys.argv:
        raise ValueError("SECRET_KEY environment variable is not set")

# ALLOWED_HOSTS - Fly.io will provide the app URL
ALLOWED_HOSTS = [
    '.fly.dev',
    'django-wingz.fly.dev',
    # Allow Fly.io internal network for health checks
    '.internal',
    'localhost',
    '127.0.0.1',
]

# Add custom domain if you have one
CUSTOM_DOMAIN = os.environ.get('CUSTOM_DOMAIN')
if CUSTOM_DOMAIN:
    ALLOWED_HOSTS.append(CUSTOM_DOMAIN)

# Allow Fly.io private IPv6 network (health checks come from here)
# Fly.io uses fdaa::/16 for private networks
import socket
try:
    # Get machine's own IP which will be in the allowed range
    hostname = socket.gethostname()
    local_ips = socket.gethostbyname_ex(hostname)[2]
    ALLOWED_HOSTS.extend(local_ips)
except Exception:
    pass

# CSRF Settings
CSRF_TRUSTED_ORIGINS = [
    'https://django-wingz.fly.dev',
]
if CUSTOM_DOMAIN:
    CSRF_TRUSTED_ORIGINS.append(f'https://{CUSTOM_DOMAIN}')

# CORS Settings - Allow frontend to access API
CORS_ALLOWED_ORIGINS = CSRF_TRUSTED_ORIGINS

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Additional locations of static files
# Map 'assets' prefix to dist/assets directory - files will be at /static/assets/
# But we also need them at /assets/ for Vite's output
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend', 'dist'),
]

# Templates configuration for serving Vue.js index.html
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'frontend', 'dist')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Use WhiteNoise for serving static files
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Serve files from root (for /assets/ to work alongside /static/)
WHITENOISE_ROOT = os.path.join(BASE_DIR, 'frontend', 'dist')

# Remove debug toolbar from installed apps
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'debug_toolbar']

# Remove debug toolbar middleware
MIDDLEWARE = [m for m in MIDDLEWARE if 'debug_toolbar' not in m]

# Security Settings
# Disable SSL redirect - Fly.io handles this at the proxy level
SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
USE_X_FORWARDED_HOST = True

# HSTS Settings
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
