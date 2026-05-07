#!/usr/bin/env python3
"""
Full system test - Tests knowledge base, RAG system, and API
"""
import os
import sys
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_knowledge_base():
    """Test knowledge base"""
    print("\n" + "="*80)
    print("TEST 1: KNOWLEDGE BASE")
    print("="*80)
    
    try:
        from knowledge_base import KNOWLEDGE_BASE, get_answer
        
        # Test a few key questions
        test_questions = [
            "What is the annual leave policy?",
            "What health insurance benefits do we have?",
            "What is the notice period for resignation?",
            "What are the WFH guidelines?",
            "What is the company mission?"
        ]
        
        all_passed = True
        for question in test_questions:
            result = get_answer(question)
            if result["answer"] != "I don't have that information in the knowledge base.":
                print(f"✓ PASS: {question}")
            else:
                print(f"✗ FAIL: {question}")
                all_passed = False
        
        if all_passed:
            print("\n✓ Knowledge Base Test: PASSED")
            return True
        else:
            print("\n✗ Knowledge Base Test: FAILED")
            return False
    
    except Exception as e:
        print(f"✗ Knowledge Base Test: ERROR - {str(e)}")
        return False


def test_rag_system():
    """Test RAG system initialization"""
    print("\n" + "="*80)
    print("TEST 2: RAG SYSTEM INITIALIZATION")
    print("="*80)
    
    try:
        from document_ingestion import initialize_pipeline
        from rag_system import create_rag_system
        
        # Initialize vector store
        print("Initializing vector store...")
        vector_store = initialize_pipeline(pdf_directory=".", rebuild=False)
        print("✓ Vector store initialized")
        
        # Initialize RAG system
        print("Initializing RAG system...")
        llm_model = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")
        temperature = float(os.getenv("TEMPERATURE", "0.7"))
        llm_provider = os.getenv("LLM_PROVIDER", "groq")
        api_key = os.getenv("GROQ_API_KEY")
        
        rag_system = create_rag_system(
            vector_store=vector_store,
            llm_model=llm_model,
            temperature=temperature,
            api_key=api_key,
            llm_provider=llm_provider
        )
        print("✓ RAG system initialized")
        
        # Test a question
        print("\nTesting RAG system with a question...")
        question = "What is the annual leave policy?"
        answer, sources = rag_system.answer_question(question)
        
        if answer and "annual leave" in answer.lower():
            print(f"✓ Got answer: {answer[:100]}...")
            print(f"✓ Sources: {len(sources)} document(s)")
            print("\n✓ RAG System Test: PASSED")
            return True
        else:
            print(f"✗ Unexpected answer: {answer}")
            print("\n✗ RAG System Test: FAILED")
            return False
    
    except Exception as e:
        print(f"✗ RAG System Test: ERROR - {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_api_endpoints():
    """Test API endpoints"""
    print("\n" + "="*80)
    print("TEST 3: API ENDPOINTS")
    print("="*80)
    
    try:
        import requests
        
        api_url = os.getenv("API_URL", "http://localhost:8000")
        
        # Test health endpoint
        print(f"Testing health endpoint: {api_url}/health")
        try:
            response = requests.get(f"{api_url}/health", timeout=5)
            if response.status_code == 200:
                print("✓ Health endpoint: OK")
            else:
                print(f"✗ Health endpoint: Status {response.status_code}")
                print("Note: API server may not be running. Start it with: python main.py")
                return None  # Skip API tests if server not running
        except requests.exceptions.ConnectionError:
            print(f"✗ Cannot connect to API at {api_url}")
            print("Note: API server is not running. Start it with: python main.py")
            return None  # Skip API tests if server not running
        
        # Test chat endpoint
        print(f"\nTesting chat endpoint: {api_url}/chat")
        test_question = "What is the annual leave policy?"
        response = requests.post(
            f"{api_url}/chat",
            json={"question": test_question},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get("answer", "")
            sources = data.get("sources", [])
            
            if answer and "annual leave" in answer.lower():
                print(f"✓ Chat endpoint: OK")
                print(f"  Answer: {answer[:100]}...")
                print(f"  Sources: {len(sources)} document(s)")
                print("\n✓ API Endpoints Test: PASSED")
                return True
            else:
                print(f"✗ Unexpected answer: {answer}")
                print("\n✗ API Endpoints Test: FAILED")
                return False
        else:
            print(f"✗ Chat endpoint: Status {response.status_code}")
            print(f"  Error: {response.json().get('detail', 'Unknown error')}")
            print("\n✗ API Endpoints Test: FAILED")
            return False
    
    except Exception as e:
        print(f"✗ API Endpoints Test: ERROR - {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("FULL SYSTEM TEST - SWS AI COMPANY ASSISTANT CHATBOT")
    print("="*80)
    
    results = {}
    
    # Test 1: Knowledge Base
    results["Knowledge Base"] = test_knowledge_base()
    
    # Test 2: RAG System
    results["RAG System"] = test_rag_system()
    
    # Test 3: API Endpoints
    api_result = test_api_endpoints()
    if api_result is not None:
        results["API Endpoints"] = api_result
    else:
        results["API Endpoints"] = "SKIPPED (Server not running)"
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    for test_name, result in results.items():
        if result is True:
            status = "✓ PASSED"
        elif result is False:
            status = "✗ FAILED"
        else:
            status = f"⊘ {result}"
        print(f"{test_name}: {status}")
    
    print("="*80)
    
    # Overall result
    passed = sum(1 for r in results.values() if r is True)
    total = len(results)
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✓ ALL TESTS PASSED - System is ready for deployment!")
        return 0
    else:
        print("\n✗ Some tests failed - Please review the errors above")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
