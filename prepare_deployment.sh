#!/bin/bash
# Django Registration System - Deployment Preparation Script
# This script prepares your Django application for deployment to Render

echo "🚀 Django Registration System - Deployment Preparation"
echo "====================================================="

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "📦 Creating virtual environment..."
    python -m venv .venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from example..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your actual values!"
fi

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Check for deployment readiness
echo "🔍 Checking deployment readiness..."
python manage.py check --deploy

echo ""
echo "✅ Preparation complete!"
echo ""
echo "📋 Next steps:"
echo "1. Edit .env file with your SECRET_KEY and settings"
echo "2. Test locally: python manage.py runserver"
echo "3. Push to GitHub: git add . && git commit -m 'Ready for deployment' && git push"
echo "4. Follow RENDER_DEPLOYMENT_GUIDE.md for deployment"
echo ""
echo "🎯 Your app will be ready for Render deployment!"