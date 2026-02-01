#!/bin/bash
set -e

echo "🚀 Starting InterVue AI build process..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Install Node.js if not available
if ! command -v node &> /dev/null; then
    echo "📦 Installing Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
    apt-get install -y nodejs
fi

# Build React frontend
echo "🔨 Building React frontend..."
cd frontend
npm ci --only=production
npm run build
cd ..

echo "✅ Build completed successfully!"