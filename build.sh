#!/bin/bash

# Build script for Render deployment

echo "🚀 Starting InterVue AI build process..."

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Check if Node.js is available, if not install it
if ! command -v node &> /dev/null; then
    echo "📦 Installing Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
fi

# Build React frontend
echo "🔨 Building React frontend..."
cd frontend
npm install
npm run build
cd ..

echo "✅ Build completed successfully!"