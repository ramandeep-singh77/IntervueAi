#!/usr/bin/env python3
"""
Railway Deployment Startup Script for InterVue AI
Ensures frontend is built and starts the FastAPI server
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def log(message):
    print(f"🚂 Railway: {message}")

def check_frontend_build():
    """Check if frontend build exists and is valid"""
    build_path = Path("frontend/build")
    index_path = build_path / "index.html"
    
    log(f"Checking frontend build at: {build_path.absolute()}")
    
    if not build_path.exists():
        log("❌ Frontend build directory not found")
        return False
    
    if not index_path.exists():
        log("❌ Frontend index.html not found")
        return False
    
    # Check if build has content
    try:
        build_contents = list(build_path.iterdir())
        log(f"✅ Frontend build found with {len(build_contents)} items")
        return True
    except Exception as e:
        log(f"❌ Error checking build directory: {e}")
        return False

def build_frontend():
    """Build the React frontend"""
    log("Building React frontend...")
    
    frontend_path = Path("frontend")
    if not frontend_path.exists():
        log("❌ Frontend directory not found")
        return False
    
    try:
        # Change to frontend directory and build
        os.chdir("frontend")
        
        # Install dependencies if node_modules doesn't exist
        if not Path("node_modules").exists():
            log("Installing npm dependencies...")
            subprocess.run(["npm", "install"], check=True)
        
        # Build the frontend
        log("Running npm build...")
        result = subprocess.run(["npm", "run", "build"], check=True, capture_output=True, text=True)
        log("✅ Frontend build completed successfully")
        
        # Change back to root directory
        os.chdir("..")
        
        return True
        
    except subprocess.CalledProcessError as e:
        log(f"❌ Frontend build failed: {e}")
        if e.stdout:
            log(f"STDOUT: {e.stdout}")
        if e.stderr:
            log(f"STDERR: {e.stderr}")
        return False
    except Exception as e:
        log(f"❌ Unexpected error during build: {e}")
        return False
    finally:
        # Ensure we're back in the root directory
        if os.getcwd().endswith("frontend"):
            os.chdir("..")

def start_server():
    """Start the FastAPI server"""
    log("Starting FastAPI server...")
    
    # Set environment variables
    os.environ.setdefault("PORT", "8000")
    os.environ.setdefault("PYTHONPATH", "/app")
    
    try:
        # Import and run the main application
        import main
        log("✅ Server started successfully")
        
    except Exception as e:
        log(f"❌ Failed to start server: {e}")
        sys.exit(1)

def main():
    """Main startup function"""
    log("Starting InterVue AI on Railway...")
    
    # Check current directory
    log(f"Current directory: {os.getcwd()}")
    log(f"Directory contents: {os.listdir('.')}")
    
    # Check if frontend build exists
    if not check_frontend_build():
        log("Frontend build not found, attempting to build...")
        
        if not build_frontend():
            log("⚠️ Frontend build failed, starting API-only mode")
        else:
            log("✅ Frontend built successfully")
    else:
        log("✅ Frontend build already exists")
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()