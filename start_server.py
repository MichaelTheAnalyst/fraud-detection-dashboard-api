"""
Quick start script for Fraud Detection Dashboard API
"""
import sys
import subprocess
from pathlib import Path


def check_requirements():
    """Check if required files exist"""
    required_files = [
        "financial_fraud_detection_dataset.csv",
        "requirements.txt",
        "backend/main.py"
    ]
    
    missing = []
    for file in required_files:
        if not Path(file).exists():
            missing.append(file)
    
    if missing:
        print("❌ Missing required files:")
        for file in missing:
            print(f"   - {file}")
        print("\n💡 Make sure 'financial_fraud_detection_dataset.csv' is in the project root.")
        return False
    
    return True


def check_dependencies():
    """Check if dependencies are installed"""
    try:
        import fastapi
        import pandas
        import uvicorn
        print("✅ Dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("\n💡 Run: pip install -r requirements.txt")
        return False


def main():
    """Main startup function"""
    print("🚀 Starting Fraud Detection Dashboard API...\n")
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check dependencies
    if not check_dependencies():
        print("\n📦 Install dependencies now? (y/n): ", end="")
        if input().lower() == 'y':
            print("\n📥 Installing dependencies...")
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        else:
            sys.exit(1)
    
    print("\n" + "="*60)
    print("🎯 FRAUD DETECTION DASHBOARD API")
    print("="*60)
    print("\n📊 Dashboard Tiles: 18")
    print("📈 Dataset: 5M transactions")
    print("⚡ Framework: FastAPI")
    print("\n" + "="*60)
    print("\n🌐 Server will start at:")
    print("   • API: http://localhost:8000")
    print("   • Docs: http://localhost:8000/docs")
    print("   • ReDoc: http://localhost:8000/redoc")
    print("   • Health: http://localhost:8000/health")
    print("\n⌨️  Press CTRL+C to stop the server")
    print("="*60 + "\n")
    
    # Start server
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "backend.main:app",
            "--reload",
            "--host", "0.0.0.0",
            "--port", "8000"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")


if __name__ == "__main__":
    main()

