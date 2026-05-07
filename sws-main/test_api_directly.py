#!/usr/bin/env python3
"""
Test API directly with sample questions
"""
import requests
import os
from dotenv import load_dotenv
import json

load_dotenv()

API_URL = os.getenv("API_URL", "http://localhost:8000")

# Test questions
test_questions = [
    "What is the annual leave policy?",
    "How many days of sick leave do employees get?",
    "What is the notice period for resignation?",
    "What are the WFH guidelines?",
    "What health insurance benefits do we have?",
    "What is the company mission?",
    "How do I apply for leave?",
    "What is the maternity leave policy?",
    "What are password requirements?",
    "What is the code of conduct policy?"
]

print("="*80)
print("TESTING API WITH SAMPLE QUESTIONS")
print("="*80)
print(f"API URL: {API_URL}\n")

passed = 0
failed = 0

for i, question in enumerate(test_questions, 1):
    try:
        response = requests.post(
            f"{API_URL}/chat",
            json={"question": question},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get("answer", "")
            sources = data.get("sources", [])
            
            # Check if answer is meaningful (not "I don't have that information")
            if "don't have that information" not in answer.lower() or len(sources) > 0:
                print(f"✓ Q{i}: {question}")
                print(f"  Answer: {answer[:100]}...")
                print(f"  Sources: {len(sources)}\n")
                passed += 1
            else:
                print(f"✗ Q{i}: {question}")
                print(f"  Answer: {answer[:100]}...")
                print(f"  Sources: {len(sources)}\n")
                failed += 1
        else:
            print(f"✗ Q{i}: {question}")
            print(f"  Error: {response.status_code} - {response.json().get('detail', 'Unknown error')}\n")
            failed += 1
    
    except Exception as e:
        print(f"✗ Q{i}: {question}")
        print(f"  Exception: {str(e)}\n")
        failed += 1

print("="*80)
print(f"RESULTS: {passed} passed, {failed} failed out of {len(test_questions)} questions")
print("="*80)
