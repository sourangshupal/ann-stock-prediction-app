#!/usr/bin/env python3
"""
Test script to verify Docker setup works correctly
"""

import requests
import time
import sys
import subprocess
import json

def check_docker_running():
    """Check if Docker is running"""
    try:
        result = subprocess.run(['docker', 'info'], 
                              capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def check_container_running(container_name):
    """Check if container is running"""
    try:
        result = subprocess.run(['docker', 'ps', '--filter', f'name={container_name}', '--format', 'json'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0 and result.stdout.strip():
            return True
        return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def test_streamlit_health(url="http://localhost:8501", timeout=60):
    """Test if Streamlit app is responding"""
    print(f"Testing Streamlit health at {url}...")
    
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Test main page
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print("✅ Main page is accessible")
                
                # Test health endpoint
                health_response = requests.get(f"{url}/_stcore/health", timeout=5)
                if health_response.status_code == 200:
                    print("✅ Health endpoint is responding")
                    return True
                else:
                    print(f"⚠️  Health endpoint returned status: {health_response.status_code}")
                    
        except requests.exceptions.RequestException as e:
            print(f"⏳ Waiting for app to start... ({int(time.time() - start_time)}s)")
            time.sleep(2)
            continue
    
    print(f"❌ App did not respond within {timeout} seconds")
    return False

def test_tensorflow_import():
    """Test if TensorFlow can be imported in the container"""
    try:
        result = subprocess.run([
            'docker', 'exec', 'ann-stock-prediction', 
            'python', '-c', 'import tensorflow as tf; print(f"TensorFlow version: {tf.__version__}")'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print(f"✅ TensorFlow import successful: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ TensorFlow import failed: {result.stderr}")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        print(f"❌ Could not test TensorFlow import: {e}")
        return False

def test_app_functionality():
    """Test basic app functionality"""
    try:
        # Test if we can access the app and it loads properly
        response = requests.get("http://localhost:8501", timeout=10)
        if "ANN Stock Prediction App" in response.text:
            print("✅ App title found in response")
            return True
        else:
            print("❌ App title not found in response")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not test app functionality: {e}")
        return False

def main():
    """Run all tests"""
    print("🐳 Docker Setup Test for ANN Stock Prediction App")
    print("=" * 50)
    
    # Test 1: Check if Docker is running
    print("\n1. Checking Docker status...")
    if not check_docker_running():
        print("❌ Docker is not running. Please start Docker and try again.")
        return False
    print("✅ Docker is running")
    
    # Test 2: Check if container is running
    print("\n2. Checking container status...")
    if not check_container_running("ann-stock-prediction"):
        print("❌ Container 'ann-stock-prediction' is not running.")
        print("💡 Try running: docker-compose up -d")
        return False
    print("✅ Container is running")
    
    # Test 3: Test Streamlit health
    print("\n3. Testing Streamlit application...")
    if not test_streamlit_health():
        print("❌ Streamlit app is not responding")
        return False
    
    # Test 4: Test TensorFlow import
    print("\n4. Testing TensorFlow in container...")
    if not test_tensorflow_import():
        print("❌ TensorFlow is not working properly")
        return False
    
    # Test 5: Test app functionality
    print("\n5. Testing app functionality...")
    if not test_app_functionality():
        print("❌ App functionality test failed")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! Your Docker setup is working correctly.")
    print("🌐 Access your app at: http://localhost:8501")
    print("📊 Try uploading sample_stock_data.csv and training a model!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
