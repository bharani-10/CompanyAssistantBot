#!/usr/bin/env python3
"""
MetaMind OS - Quick Start Script
Fast launch for immediate testing
"""
import subprocess
import sys
import os
import time
import webbrowser
from pathlib import Path

def print_banner():
    print("""
🤖 MetaMind OS - Quick Start
=============================
Fast autonomous AI software engineering system
""")

def check_dependencies():
    """Check if required dependencies are installed"""
    print("📦 Checking dependencies...")
    
    # Check Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        return False
    
    # Check if we're in the right directory
    if not os.path.exists("backend/app/main.py"):
        print("❌ Please run from the MetaMind root directory")
        return False
    
    print("✅ Dependencies check passed")
    return True

def install_backend_deps():
    """Install backend dependencies quickly"""
    print("📦 Installing backend dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "fastapi", "uvicorn[standard]", "pandas", "numpy", 
            "scikit-learn", "python-multipart", "python-dotenv"
        ], check=True, capture_output=True)
        print("✅ Backend dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Backend installation failed: {e}")
        return False

def start_backend():
    """Start the FastAPI backend"""
    print("🚀 Starting MetaMind backend...")
    
    # Change to backend directory
    os.chdir("backend")
    
    # Start uvicorn server
    process = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "app.main:app", 
        "--host", "0.0.0.0", "--port", "8000", "--reload"
    ])
    
    # Change back to root
    os.chdir("..")
    
    return process

def start_frontend():
    """Start the React frontend"""
    print("🎨 Starting MetaMind frontend...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("⚠️ Frontend directory not found, skipping...")
        return None
    
    # Check if node_modules exists
    if not (frontend_dir / "node_modules").exists():
        print("📦 Installing frontend dependencies...")
        try:
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True)
        except subprocess.CalledProcessError:
            print("❌ Frontend installation failed")
            return None
    
    # Start development server
    try:
        process = subprocess.Popen(["npm", "run", "dev"], cwd=frontend_dir)
        return process
    except FileNotFoundError:
        print("⚠️ Node.js not found, skipping frontend...")
        return None

def wait_for_server(url, timeout=30):
    """Wait for server to be ready"""
    import requests
    
    for i in range(timeout):
        try:
            response = requests.get(url, timeout=1)
            if response.status_code == 200:
                return True
        except:
            pass
        time.sleep(1)
        print(f"⏳ Waiting for server... ({i+1}/{timeout})")
    
    return False

def main():
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Install backend dependencies
    if not install_backend_deps():
        print("⚠️ Continuing without full dependencies...")
    
    # Start backend
    backend_process = start_backend()
    
    # Wait a moment for backend to start
    print("⏳ Waiting for backend to start...")
    time.sleep(3)
    
    # Check if backend is running
    try:
        import requests
        if wait_for_server("http://localhost:8000/health"):
            print("✅ Backend is running!")
        else:
            print("⚠️ Backend may not be fully ready")
    except ImportError:
        print("⚠️ Cannot verify backend status (requests not installed)")
    
    # Start frontend
    frontend_process = start_frontend()
    
    # Print status
    print("\n🎉 MetaMind OS is starting!")
    print("=" * 40)
    print("🔧 Backend API: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    if frontend_process:
        print("🎨 Frontend: http://localhost:3000")
    print("=" * 40)
    
    # Open browser
    try:
        if frontend_process:
            webbrowser.open("http://localhost:3000")
        else:
            webbrowser.open("http://localhost:8000/docs")
    except:
        pass
    
    print("\n📝 Quick Test:")
    print("1. Upload a CSV file")
    print("2. Enter a description like: 'Build a student performance prediction system'")
    print("3. Click 'Launch Autonomous Generation'")
    print("\n⚡ The system will generate a complete ML application in seconds!")
    
    try:
        print("\n🛑 Press Ctrl+C to stop all services")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping MetaMind OS...")
        
        # Terminate processes
        if backend_process:
            backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        
        print("✅ MetaMind OS stopped")

if __name__ == "__main__":
    main()