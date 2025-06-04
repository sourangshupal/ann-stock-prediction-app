#!/usr/bin/env python3
"""
Test script for FastAPI endpoints
"""

import requests
import json
import time
import os
from pathlib import Path

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_endpoint():
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed with status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_root_endpoint():
    """Test the root endpoint"""
    print("\n🔍 Testing root endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Root endpoint working: {data['message']}")
            return True
        else:
            print(f"❌ Root endpoint failed with status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Root endpoint failed: {e}")
        return False

def test_train_endpoint():
    """Test the training endpoint"""
    print("\n🔍 Testing training endpoint...")
    
    # Check if sample data exists
    sample_file = Path("data/sample_stock_data.csv")
    if not sample_file.exists():
        sample_file = Path("sample_stock_data.csv")
    
    if not sample_file.exists():
        print("❌ Sample data file not found. Creating a simple test file...")
        # Create a simple test CSV
        test_data = """Date,Open,High,Low,Close,Volume
2023-01-01,100.0,105.0,95.0,102.0,1000000
2023-01-02,101.0,106.0,96.0,103.0,1100000
2023-01-03,102.0,107.0,97.0,104.0,1200000
2023-01-04,103.0,108.0,98.0,105.0,1300000
2023-01-05,104.0,109.0,99.0,106.0,1400000
2023-01-06,105.0,110.0,100.0,107.0,1500000
2023-01-07,106.0,111.0,101.0,108.0,1600000
2023-01-08,107.0,112.0,102.0,109.0,1700000
2023-01-09,108.0,113.0,103.0,110.0,1800000
2023-01-10,109.0,114.0,104.0,111.0,1900000"""
        
        with open("test_data.csv", "w") as f:
            f.write(test_data)
        sample_file = Path("test_data.csv")
    
    try:
        with open(sample_file, 'rb') as f:
            files = {'file': ('sample_data.csv', f, 'text/csv')}
            data = {
                'epochs': 10,  # Use fewer epochs for testing
                'batch_size': 32,
                'test_split': 0.2
            }
            
            print("📤 Uploading data and starting training...")
            response = requests.post(f"{BASE_URL}/train", files=files, data=data, timeout=120)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Training successful!")
                print(f"   Model ID: {result['model_id']}")
                print(f"   Training time: {result['training_time']:.2f}s")
                print(f"   Loss: {result['loss']:.4f}")
                print(f"   MAE: {result['mae']:.4f}")
                return True, result['model_id']
            else:
                print(f"❌ Training failed with status: {response.status_code}")
                print(f"   Error: {response.text}")
                return False, None
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Training request failed: {e}")
        return False, None
    except FileNotFoundError:
        print(f"❌ Sample file not found: {sample_file}")
        return False, None

def test_predict_endpoint():
    """Test the prediction endpoint"""
    print("\n🔍 Testing prediction endpoint...")
    
    # Sample prediction data (Price, Close, High, Low, Open)
    test_features = [100.50, 101.25, 99.80, 100.75]
    
    try:
        payload = {"features": test_features}
        response = requests.post(f"{BASE_URL}/predict", json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Prediction successful!")
            print(f"   Input features: {test_features}")
            print(f"   Predicted value: {result['prediction']:.2f}")
            print(f"   Model ID: {result['model_id']}")
            return True
        else:
            print(f"❌ Prediction failed with status: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Prediction request failed: {e}")
        return False

def test_evaluate_endpoint():
    """Test the evaluation endpoint"""
    print("\n🔍 Testing evaluation endpoint...")
    
    # Use the same sample file for evaluation
    sample_file = Path("data/sample_stock_data.csv")
    if not sample_file.exists():
        sample_file = Path("sample_stock_data.csv")
    if not sample_file.exists():
        sample_file = Path("test_data.csv")
    
    try:
        with open(sample_file, 'rb') as f:
            files = {'file': ('eval_data.csv', f, 'text/csv')}
            
            print("📤 Uploading evaluation data...")
            response = requests.post(f"{BASE_URL}/evaluate", files=files, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Evaluation successful!")
                print(f"   Loss: {result['loss']:.4f}")
                print(f"   MAE: {result['mae']:.4f}")
                print(f"   Test samples: {result['test_samples']}")
                return True
            else:
                print(f"❌ Evaluation failed with status: {response.status_code}")
                print(f"   Error: {response.text}")
                return False
                
    except requests.exceptions.RequestException as e:
        print(f"❌ Evaluation request failed: {e}")
        return False
    except FileNotFoundError:
        print(f"❌ Evaluation file not found: {sample_file}")
        return False

def test_model_info_endpoint():
    """Test the model info endpoint"""
    print("\n🔍 Testing model info endpoint...")
    
    try:
        response = requests.get(f"{BASE_URL}/model/info", timeout=10)
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Model info retrieved!")
            print(f"   Model metadata: {json.dumps(result['model_metadata'], indent=2)}")
            return True
        else:
            print(f"❌ Model info failed with status: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Model info request failed: {e}")
        return False

def main():
    """Run all API tests"""
    print("🚀 FastAPI Endpoint Testing")
    print("=" * 50)
    
    # Wait for API to be ready
    print("⏳ Waiting for API to be ready...")
    max_retries = 30
    for i in range(max_retries):
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                print("✅ API is ready!")
                break
        except:
            pass
        
        if i == max_retries - 1:
            print("❌ API is not responding. Make sure it's running on port 8000")
            return False
        
        time.sleep(2)
    
    # Run tests
    tests = [
        ("Health Check", test_health_endpoint),
        ("Root Endpoint", test_root_endpoint),
        ("Training", test_train_endpoint),
        ("Prediction", test_predict_endpoint),
        ("Evaluation", test_evaluate_endpoint),
        ("Model Info", test_model_info_endpoint),
    ]
    
    results = []
    model_trained = False
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        
        if test_name == "Training":
            success, model_id = test_func()
            if success:
                model_trained = True
            results.append((test_name, success))
        elif test_name in ["Prediction", "Evaluation", "Model Info"]:
            if not model_trained:
                print(f"⏭️  Skipping {test_name} - no model trained")
                results.append((test_name, None))
                continue
            success = test_func()
            results.append((test_name, success))
        else:
            success = test_func()
            results.append((test_name, success))
    
    # Summary
    print(f"\n{'='*50}")
    print("📊 Test Results Summary:")
    print(f"{'='*50}")
    
    for test_name, result in results:
        if result is True:
            status = "✅ PASSED"
        elif result is False:
            status = "❌ FAILED"
        else:
            status = "⏭️  SKIPPED"
        print(f"{test_name:20} {status}")
    
    passed = sum(1 for _, result in results if result is True)
    total = sum(1 for _, result in results if result is not None)
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Your FastAPI server is working correctly.")
        print(f"🌐 Access Swagger UI at: {BASE_URL}/docs")
        print(f"📚 Access ReDoc at: {BASE_URL}/redoc")
    else:
        print(f"\n⚠️  Some tests failed. Check the logs above for details.")
    
    # Cleanup
    if os.path.exists("test_data.csv"):
        os.remove("test_data.csv")
        print("\n🧹 Cleaned up test files")

if __name__ == "__main__":
    main()
