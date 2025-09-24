#!/bin/sh
set -e

echo "Running database migrations..."

if python manage.py showmigrations --plan | grep -q '\[ \]'; then
    echo "Found pending migrations:"
    python manage.py showmigrations --plan | grep '\[ \]'

    python manage.py migrate --noinput
    echo "Migrations completed successfully"
else
    echo "No pending migrations found"
fi