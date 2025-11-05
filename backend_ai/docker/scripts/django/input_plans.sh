#!/bin/sh
set -e

echo "Inputting predefined plans..."
python manage.py init_plans
echo "Input plans completed successfully"

