#!/usr/bin/env python3
"""
InterVue AI - Railway Startup Script
Ensures proper initialization and environment setup
"""

import os
import sys
import subprocess
from pathlib import Path

def setup_environment():
    """Setup environment for Railway deployment"""
    print("🚂 Starting InterVue AI on Railway...")
    
    # Set Python path
    backend_path = Path(__file__).parent / "backend"
    if str(backend_path) not in sys.path:
        sys.path.insert(0, str(backend_path))
    
    # Check for required environment variables
    required_vars = ["GEMINI_API_KEY"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"⚠️  Warning: Missing environment variables: {missing_vars}")
        print("   The app will run in demo mode without AI features")
    else:
        print("✅ All required environment variables found")
    
    # Check if frontend build exists
    frontend_build = Path("frontend/build")
    if frontend_build.exists():
        print("✅ Frontend build found")
    else:
        print("⚠️  Frontend build not found - API only mode")
    
    print("🚀 Starting FastAPI server...")

if __name__ == "__main__":
    setup_environment()
    
    # Import and run the main application
    from main import app
    import uvicorn
    
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)