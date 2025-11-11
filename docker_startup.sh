#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

PORT=${PORT:-8000}

echo "Starting Django application..."
echo "Running on port: $PORT"

# Start gunicorn
exec gunicorn --bind 0.0.0.0:$PORT \
    --workers 2 \
    --threads 4 \
    --timeout 60 \
    --access-logfile - \
    --error-logfile - \
    config.wsgi:application
