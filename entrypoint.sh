#!/bin/sh
set -e

echo "Waiting for DB and running migrations..."
# Optional: add wait-for-db logic for remote DBs
python manage.py makemigrations --noinput || true
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

if [ "$DJANGO_DEVELOPMENT" = "1" ]; then
  echo "Starting Django development server..."
  python manage.py runserver 0.0.0.0:8000
else
  echo "Starting Gunicorn..."
  exec gunicorn credit_risk.wsgi:application --bind 0.0.0.0:8000 --workers 3
fi