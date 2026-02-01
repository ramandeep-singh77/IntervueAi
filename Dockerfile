# Use Python 3.9 as base image
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    ffmpeg \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js 18
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Verify installations
RUN python --version && node --version && npm --version

# Set working directory
WORKDIR /app

# Copy Python requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend package files first
COPY frontend/package*.json ./frontend/
WORKDIR /app/frontend
RUN npm install --production=false

# Copy all source code
WORKDIR /app
COPY . .

# Build React frontend with verbose output
WORKDIR /app/frontend
RUN npm run build && ls -la build/

# Verify build was successful
RUN test -d build && test -f build/index.html && echo "✅ Frontend build successful" || echo "❌ Frontend build failed"

# Back to app directory
WORKDIR /app

# Expose port
EXPOSE 8000

# Start command
CMD ["python", "main.py"]