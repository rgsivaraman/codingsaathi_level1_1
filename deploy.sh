#!/bin/bash

# Agent Marketplace Deployment Script

echo "🚀 Starting Agent Marketplace Deployment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Stop existing containers
echo "📦 Stopping existing containers..."
docker-compose down

# Remove old images (optional)
read -p "Do you want to remove old images? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🗑️  Removing old images..."
    docker-compose down --rmi all
fi

# Build and start containers
echo "🔨 Building containers..."
docker-compose build

echo "▶️  Starting containers..."
docker-compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are running
if docker-compose ps | grep -q "Up"; then
    echo "✅ Deployment successful!"
    echo ""
    echo "📍 Access the application at:"
    echo "   Frontend: http://localhost"
    echo "   Backend API: http://localhost:8000"
    echo "   API Docs: http://localhost:8000/docs"
    echo ""
    echo "📝 View logs with: docker-compose logs -f"
    echo "🛑 Stop services with: docker-compose down"
else
    echo "❌ Deployment failed. Check logs with: docker-compose logs"
    exit 1
fi
