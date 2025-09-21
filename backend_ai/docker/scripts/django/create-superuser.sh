#!/bin/bash
set -e

echo "Checking for existing superuser..."


SUPERUSER_EXISTS=$(python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
print(User.objects.filter(is_superuser=True).exists())
" | tail -n1)

if [ "$SUPERUSER_EXISTS" = "True" ]; then
    echo "Superuser already exists, skipping creation"
    exit 0
fi

echo "Creating superuser..."
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()

username = '${DJANGO_SUPERUSER_USERNAME:-admin}'
email = '${DJANGO_SUPERUSER_EMAIL:-admin@example.com}'
password = '${DJANGO_SUPERUSER_PASSWORD:-admin123}'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser {username} created successfully')
else:
    print(f'User {username} already exists')
"