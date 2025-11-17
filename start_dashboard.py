#!/usr/bin/env python3
"""
Automated Dashboard Startup Script
Starts both backend API and frontend React app simultaneously

Author: Masood Nazari
GitHub: github.com/michaeltheanalyst
"""

import subprocess
import sys
import os
import time
import platform
from pathlib import Path

def print_banner():
    """Print startup banner"""
    banner = """
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║        🚀 FRAUD DETECTION DASHBOARD - AUTO STARTUP 🚀          ║
║                                                                ║
║  Backend API + Frontend React Dashboard                       ║
║  Author: Masood Nazari                                         ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_python_version():
    """Check Python version"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9+ required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]}")
    return True

def check_node():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], 
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ Node.js not found")
    print("   Install from: https://nodejs.org/")
    return False

def check_npm():
    """Check if npm is installed"""
    try:
        result = subprocess.run(['npm', '--version'], 
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            print(f"✅ npm {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("❌ npm not found")
    return False

def check_backend_dependencies():
    """Check if backend dependencies are installed"""
    try:
        import fastapi
        import pandas
        import uvicorn
        print("✅ Backend dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing backend dependency: {e.name}")
        print("   Run: pip install -r requirements.txt")
        return False

def check_frontend_dependencies():
    """Check if frontend dependencies are installed"""
    frontend_path = Path("frontend")
    node_modules = frontend_path / "node_modules"
    
    if node_modules.exists():
        print("✅ Frontend dependencies installed")
        return True
    else:
        print("⚠️  Frontend dependencies not installed")
        print("   Installing now...")
        return install_frontend_dependencies()

def install_frontend_dependencies():
    """Install frontend dependencies"""
    frontend_path = Path("frontend")
    
    if not frontend_path.exists():
        print("❌ Frontend directory not found")
        return False
    
    print("📦 Installing frontend dependencies (this may take a minute)...")
    
    try:
        process = subprocess.run(
            ['npm', 'install'],
            cwd=str(frontend_path),
            capture_output=True,
            text=True
        )
        
        if process.returncode == 0:
            print("✅ Frontend dependencies installed successfully")
            return True
        else:
            print(f"❌ Installation failed: {process.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def check_dataset():
    """Check if dataset exists"""
    dataset = Path("financial_fraud_detection_dataset.csv")
    if dataset.exists():
        size_mb = dataset.stat().st_size / (1024 * 1024)
        print(f"✅ Dataset found ({size_mb:.1f} MB)")
        return True
    else:
        print("⚠️  Dataset not found")
        print("   Place 'financial_fraud_detection_dataset.csv' in project root")
        return False

def start_backend():
    """Start the backend API server"""
    print("\n" + "="*60)
    print("🔧 Starting Backend API Server...")
    print("="*60)
    
    # Determine the appropriate command based on OS
    if platform.system() == "Windows":
        # Windows: Use PowerShell to start in new window
        cmd = [
            'powershell', '-Command',
            'Start-Process', 'python', 
            '-ArgumentList', '"-m", "uvicorn", "backend.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"',
            '-NoNewWindow'
        ]
    else:
        # Unix: Use terminal command
        cmd = [
            sys.executable, '-m', 'uvicorn',
            'backend.main:app',
            '--reload',
            '--host', '0.0.0.0',
            '--port', '8000'
        ]
    
    try:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        
        print("⏳ Waiting for backend to start...")
        time.sleep(3)
        
        if process.poll() is None:
            print("✅ Backend API started successfully")
            print("   📍 API: http://localhost:8000")
            print("   📖 Docs: http://localhost:8000/docs")
            return process
        else:
            print("❌ Backend failed to start")
            return None
    except Exception as e:
        print(f"❌ Error starting backend: {str(e)}")
        return None

def start_frontend():
    """Start the frontend React app"""
    print("\n" + "="*60)
    print("🎨 Starting Frontend React App...")
    print("="*60)
    
    frontend_path = Path("frontend")
    
    if not frontend_path.exists():
        print("❌ Frontend directory not found")
        return None
    
    try:
        if platform.system() == "Windows":
            # Windows
            process = subprocess.Popen(
                ['npm.cmd', 'run', 'dev'],
                cwd=str(frontend_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                creationflags=subprocess.CREATE_NEW_CONSOLE if platform.system() == "Windows" else 0
            )
        else:
            # Unix
            process = subprocess.Popen(
                ['npm', 'run', 'dev'],
                cwd=str(frontend_path),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
        
        print("⏳ Waiting for frontend to start...")
        time.sleep(5)
        
        if process.poll() is None:
            print("✅ Frontend app started successfully")
            print("   📍 Dashboard: http://localhost:3000")
            return process
        else:
            print("❌ Frontend failed to start")
            return None
    except Exception as e:
        print(f"❌ Error starting frontend: {str(e)}")
        return None

def print_success():
    """Print success message with URLs"""
    success_msg = """
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║                  ✅ DASHBOARD STARTED SUCCESSFULLY! ✅          ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

🌐 Access Points:
   
   📊 Dashboard:     http://localhost:3000
   🔌 Backend API:   http://localhost:8000
   📖 API Docs:      http://localhost:8000/docs
   💚 Health Check:  http://localhost:8000/health

⌨️  Commands:
   
   Press Ctrl+C to stop both servers
   
🎯 Quick Actions:
   
   1. Open http://localhost:3000 in your browser
   2. View real-time fraud detection data
   3. Explore 6 interactive dashboard tiles
   4. Check API documentation at /docs

📧 Support: M.Nazari@soton.ac.uk
🔗 GitHub: github.com/michaeltheanalyst

════════════════════════════════════════════════════════════════
"""
    print(success_msg)

def main():
    """Main startup function"""
    print_banner()
    
    print("\n🔍 Pre-flight Checks...\n")
    
    # Run checks
    checks = [
        ("Python Version", check_python_version()),
        ("Node.js", check_node()),
        ("npm", check_npm()),
        ("Backend Dependencies", check_backend_dependencies()),
        ("Frontend Dependencies", check_frontend_dependencies()),
        ("Dataset", check_dataset()),
    ]
    
    # Check if all passed
    all_passed = all(result for _, result in checks)
    
    if not all_passed:
        print("\n❌ Pre-flight checks failed!")
        print("   Please fix the issues above and try again.")
        return 1
    
    print("\n✅ All pre-flight checks passed!\n")
    
    # Start servers
    backend_process = start_backend()
    if not backend_process:
        print("\n❌ Failed to start backend. Exiting...")
        return 1
    
    frontend_process = start_frontend()
    if not frontend_process:
        print("\n❌ Failed to start frontend. Stopping backend...")
        backend_process.terminate()
        return 1
    
    print_success()
    
    # Keep running and handle shutdown
    try:
        while True:
            time.sleep(1)
            
            # Check if processes are still running
            if backend_process.poll() is not None:
                print("\n⚠️  Backend process stopped unexpectedly")
                break
            
            if frontend_process.poll() is not None:
                print("\n⚠️  Frontend process stopped unexpectedly")
                break
                
    except KeyboardInterrupt:
        print("\n\n⏹️  Shutting down dashboard...")
        print("   Stopping backend...")
        backend_process.terminate()
        print("   Stopping frontend...")
        frontend_process.terminate()
        
        # Wait for processes to terminate
        backend_process.wait(timeout=5)
        frontend_process.wait(timeout=5)
        
        print("\n✅ Dashboard stopped successfully")
        print("👋 Goodbye!\n")
        return 0
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\n❌ Unexpected error: {str(e)}")
        sys.exit(1)

