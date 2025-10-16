#!/bin/sh
set -e

echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 1
done
echo "Database ready"

echo "Waiting for Redis..."
while ! nc -z redis 6379; do
  sleep 1
done
echo "Redis ready"

if [ "$RUN_MIGRATIONS" = "true" ]; then
  /app/docker/scripts/django/migrate.sh
fi

if [ "$CREATE_SUPERUSER" = "true" ]; then
  /app/docker/scripts/django/create-superuser.sh
fi

if [ "$INIT_PLANS" = "true" ]; then
  /app/docker/scripts/django/input_plans.sh
fi
exec "$@"