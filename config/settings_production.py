"""
Production settings for Fly.io deployment
"""
import os
import dj_database_url
from .settings import *

# SECURITY
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')

if not SECRET_KEY:
    raise ValueError("SECRET_KEY environment variable is not set")

# ALLOWED_HOSTS - Fly.io will provide the app URL
ALLOWED_HOSTS = [
    '.fly.dev',
    'wingz-ride-management.fly.dev',
]

# Add custom domain if you have one
CUSTOM_DOMAIN = os.environ.get('CUSTOM_DOMAIN')
if CUSTOM_DOMAIN:
    ALLOWED_HOSTS.append(CUSTOM_DOMAIN)

# CSRF Settings
CSRF_TRUSTED_ORIGINS = [
    'https://wingz-ride-management.fly.dev',
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
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend', 'dist', 'assets'),
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

# Remove debug toolbar from installed apps
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'debug_toolbar']

# Remove debug toolbar middleware
MIDDLEWARE = [m for m in MIDDLEWARE if 'debug_toolbar' not in m]

# Security Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

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
