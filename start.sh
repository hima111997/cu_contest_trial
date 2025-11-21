#!/bin/bash
echo "Starting deployment setup..."

# Install dependencies if not already installed
echo "Installing dependencies..."
pip install -r requirements.txt

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --run-syncdb

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Setup complete! Starting web server..."
# Start Gunicorn
gunicorn registration_system.wsgi --log-file -