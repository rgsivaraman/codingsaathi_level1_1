#!/bin/bash

# Agent Marketplace - Online Deployment Helper Script
# This script helps deploy the application to Railway.app

set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        Agent Marketplace - Online Deployment Setup            ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "📦 Railway CLI not found. Installing..."
    echo ""
    echo "Please install Railway CLI first:"
    echo ""
    echo "  Mac/Linux:"
    echo "    bash <(curl -fsSL cli.new)"
    echo ""
    echo "  Or visit: https://docs.railway.app/develop/cli"
    echo ""
    echo "After installation, run this script again."
    exit 1
fi

echo "✅ Railway CLI found!"
echo ""

# Check if user is logged in
if ! railway whoami &> /dev/null; then
    echo "🔐 Please login to Railway..."
    railway login
    echo ""
fi

echo "✅ Logged in to Railway!"
echo ""

# Create a new project
echo "🚀 Creating new Railway project..."
echo ""

# Initialize Railway project
if [ ! -f "railway.json" ]; then
    railway init
else
    echo "⚠️  railway.json already exists, using existing configuration"
fi

echo ""
echo "📊 Current status:"
railway status
echo ""

# Add PostgreSQL
echo "🗄️  Adding PostgreSQL database..."
railway add --database postgres

echo ""
echo "🔧 Configuring environment variables..."
echo ""

# Generate secret key
SECRET_KEY=$(openssl rand -hex 32)

# Set environment variables for backend
echo "Setting backend environment variables..."
railway variables set DATABASE_URL='${{Postgres.DATABASE_URL}}'
railway variables set SECRET_KEY="$SECRET_KEY"
railway variables set ALLOWED_ORIGINS='https://*.railway.app,https://*.up.railway.app'
railway variables set ACCESS_TOKEN_EXPIRE_MINUTES=30

echo ""
echo "✅ Environment variables configured!"
echo ""

# Deploy
echo "🚀 Deploying to Railway..."
echo "This may take 5-10 minutes..."
echo ""

railway up

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                  Deployment Complete! 🎉                       ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Get your deployment URL:"
echo "   railway open"
echo ""
echo "2. View deployment logs:"
echo "   railway logs"
echo ""
echo "3. Check service status:"
echo "   railway status"
echo ""
echo "4. Configure frontend (if separate):"
echo "   - Set REACT_APP_API_URL to your backend URL"
echo "   - Deploy frontend to Vercel or Railway"
echo ""
echo "📖 Full guide: See DEPLOY_ONLINE.md"
echo ""
