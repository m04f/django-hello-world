#!/usr/bin/env bash
# Exit on error
set -o errexit

pip install -r requirements.txt

pip install 'uvicorn[standard]' gunicorn

# Apply any outstanding database migrations
python manage.py migrate
