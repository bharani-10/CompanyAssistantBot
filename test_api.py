#!/usr/bin/env python3
"""
Test script to verify MetaMind API functionality
"""
import requests
import json
import os

def test_api_health():
    """Test if the API is responding"""
    try:
        response = requests.get("http://localhost:8000/docs")
        print(f"✅ API Health Check: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ API Health Check Failed: {e}")
        return False

def test_upload_endpoint():
    """Test file upload functionality"""
    try:
        # Check if test data exists
        test_file = "data/students_performance.csv"
        if not os.path.exists(test_file):
            print(f"❌ Test data not found: {test_file}")
            return False
        
        with open(test_file, 'rb') as f:
            files = {'file': ('students_performance.csv', f, 'text/csv')}
            response = requests.post("http://localhost:8000/upload", files=files)
        
        print(f"✅ Upload Test: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Uploaded: {result.get('filename')}")
            print(f"   Path: {result.get('path')}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Upload Test Failed: {e}")
        return False

def test_run_endpoint():
    """Test analysis run endpoint"""
    try:
        payload = {
            "dataset_path": "uploads/students_performance.csv",
            "instruction": "Predict student performance using machine learning"
        }
        response = requests.post("http://localhost:8000/run", params=payload)
        print(f"✅ Run Analysis Test: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Message: {result.get('message')}")
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Run Analysis Test Failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing MetaMind API...")
    print("=" * 50)
    
    tests = [
        ("API Health", test_api_health),
        ("File Upload", test_upload_endpoint),
        ("Analysis Run", test_run_endpoint)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n🔍 Testing {test_name}...")
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"   {test_name}: {status}")
    
    all_passed = all(result for _, result in results)
    print(f"\n🎯 Overall: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")