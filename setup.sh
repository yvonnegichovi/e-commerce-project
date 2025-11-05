#!/bin/bash
# Quick start script for local development without Docker

set -e

echo "🚀 Starting E-Commerce API Setup..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from example..."
    cp .env.example .env
    echo "⚠️  Please update .env with your database and Redis URLs"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start the server:"
echo "  1. Make sure PostgreSQL and Redis are running"
echo "  2. Update .env with your database credentials"
echo "  3. Run: uvicorn app.main:app --reload"
echo ""
echo "Or use Docker Compose:"
echo "  docker-compose up -d"
echo ""
echo "API will be available at: http://localhost:8000"
echo "Swagger docs at: http://localhost:8000/docs"
