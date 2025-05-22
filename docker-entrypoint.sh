#!/bin/bash

# Set default values for environment variables
export DB_ENGINE=${DB_ENGINE:-django.db.backends.postgresql}
export DB_NAME=${DB_NAME:-iop_db}
export DB_USER=${DB_USER:-postgres}
export DB_PASSWORD=${DB_PASSWORD:-postgres}
export DB_HOST=${DB_HOST:-db}
export DB_PORT=${DB_PORT:-5432}
export STATIC_ROOT=${STATIC_ROOT:-/app/static}
export MEDIA_ROOT=${MEDIA_ROOT:-/app/media}

# Function to check if a variable is set
check_env_var() {
    if [ -z "${!1}" ]; then
        echo "Error: $1 is not set"
        exit 1
    fi
}

# Check required environment variables
required_vars=(
    "DB_ENGINE"
    "DB_NAME"
    "DB_USER"
    "DB_PASSWORD"
    "DB_HOST"
    "DB_PORT"
    "STATIC_ROOT"
    "MEDIA_ROOT"
)

for var in "${required_vars[@]}"; do
    check_env_var "$var"
done

# Wait for database to be ready
echo "Waiting for database..."
while ! nc -z $DB_HOST $DB_PORT; do
    sleep 0.1
done
echo "Database is ready!"

# Create necessary directories
mkdir -p $STATIC_ROOT $MEDIA_ROOT

# Run migrations
echo "Running migrations..."
python manage.py migrate

# Create superuser if DJANGO_SUPERUSER_* variables are set
if [ ! -z "$DJANGO_SUPERUSER_EMAIL" ] && [ ! -z "$DJANGO_SUPERUSER_PASSWORD" ]; then
    echo "Creating superuser..."
    python manage.py createsuperuser \
        --email "$DJANGO_SUPERUSER_EMAIL" \
        --noinput
    # Set password separately to avoid password validation issues
    python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').update(password='$DJANGO_SUPERUSER_PASSWORD')"
fi

# Seed initial data
echo "Seeding initial data..."
python manage.py seed_groups
python manage.py seed_roles
python manage.py seed_countries

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000 