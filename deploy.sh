#!/bin/bash
# Deployment script for Learning Platform
# This script pulls the latest code, builds the frontend, and restarts the application
# Usage: ./deploy.sh

set -e  # Exit on any error

echo "========================================="
echo "Starting deployment..."
echo "========================================="

# Navigate to project directory
cd /var/www/learningplatform

# Pull latest code from git
echo ""
echo "Pulling latest code from git..."
git pull origin main

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source .venv/bin/activate

# Load environment variables
echo ""
echo "Loading environment variables..."
export $(cat .env.production | xargs)

# Install/update Python dependencies
echo ""
echo "Installing Python dependencies..."
uv pip install -r pyproject.toml

# Build frontend
echo ""
echo "Building frontend..."
cd frontend
npm ci --production=false
npm run build
cp -r dist/production/* ../learningplatform/static/frontend/
cd ..

# Collect static files
echo ""
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo ""
echo "Running database migrations..."
python manage.py migrate --noinput

# Clear old log files (keep last 30 days)
echo ""
echo "Cleaning up old log files..."
find logs/ -name "*.log" -mtime +30 -delete 2>/dev/null || true

# Restart Gunicorn
echo ""
echo "Restarting application..."
sudo systemctl restart learningplatform

# Wait a moment for the service to start
sleep 2

# Check if the service is running
echo ""
if sudo systemctl is-active --quiet learningplatform; then
    echo "✓ Application restarted successfully!"
else
    echo "✗ WARNING: Application may not have started correctly"
    echo "  Check status with: sudo systemctl status learningplatform"
fi

echo ""
echo "========================================="
echo "Deployment completed successfully!"
echo "========================================="
echo ""
echo "Next steps:"
echo "  - Check logs: sudo journalctl -u learningplatform -f"
echo "  - View status: sudo systemctl status learningplatform"
echo "  - Test site: https://your-domain.com"
echo ""
