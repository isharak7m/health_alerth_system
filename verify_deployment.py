"""
Deployment Verification Script
Run this to verify all services are working correctly
"""
import requests
import sys
import os
from dotenv import load_dotenv

load_dotenv()

def check_backend(url):
    """Check if backend is responding"""
    try:
        response = requests.get(f"{url}/", timeout=10)
        if response.status_code == 200:
            print(f"✅ Backend is live: {url}")
            return True
        else:
            print(f"❌ Backend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        return False

def check_frontend(url):
    """Check if frontend is responding"""
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            print(f"✅ Frontend is live: {url}")
            return True
        else:
            print(f"❌ Frontend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend connection failed: {e}")
        return False

def check_database():
    """Check if database connection works"""
    try:
        from backend.app.database import engine
        connection = engine.connect()
        connection.close()
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def check_ollama(url="http://localhost:11434"):
    """Check if Ollama is running"""
    try:
        response = requests.get(f"{url}/api/tags", timeout=5)
        if response.status_code == 200:
            print(f"✅ Ollama is running: {url}")
            models = response.json().get('models', [])
            if models:
                print(f"   Available models: {', '.join([m['name'] for m in models])}")
            return True
        else:
            print(f"❌ Ollama returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"⚠️  Ollama not running (optional for deployment): {e}")
        return False

def main():
    print("=" * 60)
    print("Health Monitoring System - Deployment Verification")
    print("=" * 60)
    print()
    
    # Get URLs from environment or prompt
    backend_url = os.getenv("BACKEND_URL") or input("Enter backend URL (e.g., https://your-app.onrender.com): ").strip()
    frontend_url = os.getenv("FRONTEND_URL") or input("Enter frontend URL (e.g., https://your-app.vercel.app): ").strip()
    
    print()
    print("Checking services...")
    print("-" * 60)
    
    results = []
    
    # Check backend
    results.append(("Backend", check_backend(backend_url)))
    
    # Check frontend
    results.append(("Frontend", check_frontend(frontend_url)))
    
    # Check database (if running locally)
    if os.path.exists("backend/app/database.py"):
        results.append(("Database", check_database()))
    
    # Check Ollama (optional)
    results.append(("Ollama (Local)", check_ollama()))
    
    print()
    print("=" * 60)
    print("Verification Summary")
    print("=" * 60)
    
    for service, status in results:
        status_icon = "✅" if status else "❌"
        print(f"{status_icon} {service}")
    
    print()
    
    all_critical_passed = results[0][1] and results[1][1]  # Backend and Frontend
    
    if all_critical_passed:
        print("🎉 All critical services are operational!")
        print()
        print("Your application is live at:")
        print(f"   Frontend: {frontend_url}")
        print(f"   Backend:  {backend_url}")
        print(f"   API Docs: {backend_url}/docs")
        return 0
    else:
        print("⚠️  Some critical services are not responding.")
        print("   Check the deployment logs and configuration.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
