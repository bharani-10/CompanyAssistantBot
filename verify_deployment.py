#!/usr/bin/env python3
"""
Deployment verification script
Checks all configurations and dependencies before deployment
"""

import os
import sys
import subprocess
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{Colors.END}\n")

def print_success(text):
    print(f"{Colors.GREEN}✓ {text}{Colors.END}")

def print_error(text):
    print(f"{Colors.RED}✗ {text}{Colors.END}")

def print_warning(text):
    print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")

def check_python_version():
    """Check Python version"""
    print_header("Python Version Check")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print_success(f"Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print_error(f"Python 3.8+ required, found {version.major}.{version.minor}")
        return False

def check_dependencies():
    """Check if all required packages are installed"""
    print_header("Dependencies Check")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'streamlit',
        'langchain',
        'langchain_google_genai',
        'langchain_openai',
        'langchain_community',
        'chromadb',
        'sentence_transformers',
        'pydantic',
        'dotenv',
        'pypdf',
        'requests',
        'google.generativeai'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print_success(f"{package}")
        except ImportError:
            print_error(f"{package}")
            missing.append(package)
    
    if missing:
        print_warning(f"\nMissing packages: {', '.join(missing)}")
        print(f"Install with: pip install -r requirements.txt")
        return False
    
    return True

def check_environment_variables():
    """Check if required environment variables are set"""
    print_header("Environment Variables Check")
    
    required_vars = {
        'GEMINI_API_KEY': 'Google Gemini API Key',
        'LLM_MODEL': 'LLM Model Name',
        'LLM_PROVIDER': 'LLM Provider',
    }
    
    optional_vars = {
        'OPENAI_API_KEY': 'OpenAI API Key (optional)',
        'API_HOST': 'API Host',
        'API_PORT': 'API Port',
        'API_URL': 'API URL',
        'PDF_DIRECTORY': 'PDF Directory',
        'CHROMA_PERSIST_DIRECTORY': 'ChromaDB Directory',
    }
    
    all_good = True
    
    print("Required Variables:")
    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            masked_value = value[:10] + "***" if len(value) > 10 else "***"
            print_success(f"{var}: {masked_value}")
        else:
            print_error(f"{var}: NOT SET")
            all_good = False
    
    print("\nOptional Variables:")
    for var, description in optional_vars.items():
        value = os.getenv(var)
        if value:
            print_success(f"{var}: {value}")
        else:
            print_warning(f"{var}: NOT SET (using default)")
    
    return all_good

def check_pdf_files():
    """Check if PDF files exist"""
    print_header("PDF Files Check")
    
    pdf_dir = os.getenv("PDF_DIRECTORY", ".")
    
    if not os.path.exists(pdf_dir):
        print_error(f"PDF directory not found: {pdf_dir}")
        return False
    
    pdf_files = list(Path(pdf_dir).glob("*.pdf"))
    
    if not pdf_files:
        print_warning(f"No PDF files found in {pdf_dir}")
        return False
    
    print_success(f"Found {len(pdf_files)} PDF files:")
    for pdf_file in sorted(pdf_files):
        size_mb = os.path.getsize(pdf_file) / (1024 * 1024)
        print(f"  - {pdf_file.name} ({size_mb:.2f} MB)")
    
    return True

def check_file_structure():
    """Check if all required files exist"""
    print_header("File Structure Check")
    
    required_files = [
        'app.py',
        'main.py',
        'document_ingestion.py',
        'rag_system.py',
        'utils.py',
        'config.py',
        'requirements.txt',
        '.env.example',
    ]
    
    all_good = True
    for file in required_files:
        if os.path.exists(file):
            print_success(file)
        else:
            print_error(file)
            all_good = False
    
    return all_good

def check_syntax():
    """Check Python syntax"""
    print_header("Python Syntax Check")
    
    python_files = [
        'app.py',
        'main.py',
        'document_ingestion.py',
        'rag_system.py',
        'utils.py',
        'config.py',
    ]
    
    all_good = True
    for file in python_files:
        try:
            with open(file, 'r') as f:
                compile(f.read(), file, 'exec')
            print_success(file)
        except SyntaxError as e:
            print_error(f"{file}: {e}")
            all_good = False
    
    return all_good

def check_imports():
    """Check if all imports work"""
    print_header("Import Check")
    
    try:
        print("Checking app.py imports...")
        import app
        print_success("app.py imports OK")
    except Exception as e:
        print_error(f"app.py: {e}")
        return False
    
    try:
        print("Checking main.py imports...")
        import main
        print_success("main.py imports OK")
    except Exception as e:
        print_error(f"main.py: {e}")
        return False
    
    try:
        print("Checking document_ingestion.py imports...")
        import document_ingestion
        print_success("document_ingestion.py imports OK")
    except Exception as e:
        print_error(f"document_ingestion.py: {e}")
        return False
    
    try:
        print("Checking rag_system.py imports...")
        import rag_system
        print_success("rag_system.py imports OK")
    except Exception as e:
        print_error(f"rag_system.py: {e}")
        return False
    
    return True

def check_api_health():
    """Check if API is running"""
    print_header("API Health Check")
    
    api_url = os.getenv("API_URL", "http://localhost:8000")
    
    try:
        import requests
        response = requests.get(f"{api_url}/health", timeout=2)
        if response.status_code == 200:
            print_success(f"API is running at {api_url}")
            return True
        else:
            print_warning(f"API returned status {response.status_code}")
            return False
    except Exception as e:
        print_warning(f"API not running (this is OK if not started yet): {e}")
        return False

def main():
    """Run all checks"""
    print(f"\n{Colors.BLUE}")
    print("╔════════════════════════════════════════════════════════════╗")
    print("║   SWS AI Company Assistant - Deployment Verification      ║")
    print("╚════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}")
    
    checks = [
        ("Python Version", check_python_version),
        ("File Structure", check_file_structure),
        ("Python Syntax", check_syntax),
        ("Dependencies", check_dependencies),
        ("Environment Variables", check_environment_variables),
        ("PDF Files", check_pdf_files),
        ("Imports", check_imports),
        ("API Health", check_api_health),
    ]
    
    results = {}
    for name, check_func in checks:
        try:
            results[name] = check_func()
        except Exception as e:
            print_error(f"Error during {name}: {e}")
            results[name] = False
    
    # Summary
    print_header("Verification Summary")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "PASS" if result else "FAIL"
        color = Colors.GREEN if result else Colors.RED
        print(f"{color}[{status}]{Colors.END} {name}")
    
    print(f"\n{Colors.BLUE}Result: {passed}/{total} checks passed{Colors.END}")
    
    if passed == total:
        print(f"\n{Colors.GREEN}✓ All checks passed! Ready for deployment.{Colors.END}\n")
        return 0
    else:
        print(f"\n{Colors.RED}✗ Some checks failed. Please fix the issues above.{Colors.END}\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
