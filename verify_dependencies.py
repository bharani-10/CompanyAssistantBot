#!/usr/bin/env python3
"""
Dependency Verification Script
Verifies that all packages are installed with correct versions
"""

import sys
import subprocess

# Expected versions (from requirements.txt)
EXPECTED_VERSIONS = {
    'fastapi': '0.104.1',
    'uvicorn': '0.24.0',
    'streamlit': '1.28.1',
    'langchain': '0.1.14',
    'langchain-text-splitters': '0.0.1',
    'langchain-groq': '0.1.3',
    'langchain-google-genai': '0.0.13',
    'langchain-openai': '0.1.8',
    'langchain-community': '0.0.38',
    'chromadb': '0.4.24',
    'sentence-transformers': '2.2.2',
    'pydantic': '2.5.3',
    'numpy': '1.26.4',
    'pandas': '2.1.4',
    'pypdf': '3.17.1',
    'python-dotenv': '1.0.0',
    'requests': '2.31.0',
    'google-generativeai': '0.3.0',
}

def get_installed_version(package_name):
    """Get installed version of a package"""
    try:
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'show', package_name],
            capture_output=True,
            text=True
        )
        for line in result.stdout.split('\n'):
            if line.startswith('Version:'):
                return line.split('Version:')[1].strip()
    except:
        pass
    return None

def verify_imports():
    """Verify all critical imports work"""
    print("\n" + "="*80)
    print("VERIFYING IMPORTS")
    print("="*80)
    
    imports_to_test = [
        ('streamlit', 'Streamlit'),
        ('fastapi', 'FastAPI'),
        ('langchain', 'LangChain'),
        ('langchain_community', 'LangChain Community'),
        ('chromadb', 'ChromaDB'),
        ('sentence_transformers', 'Sentence Transformers'),
        ('numpy', 'NumPy'),
        ('pandas', 'Pandas'),
        ('pydantic', 'Pydantic'),
    ]
    
    all_passed = True
    for module_name, display_name in imports_to_test:
        try:
            __import__(module_name)
            print(f"✅ {display_name}: OK")
        except ImportError as e:
            print(f"❌ {display_name}: FAILED - {str(e)}")
            all_passed = False
    
    return all_passed

def main():
    print("\n" + "="*80)
    print("DEPENDENCY VERIFICATION SCRIPT")
    print("="*80)
    
    print("\nPython Version:", sys.version)
    print("Python Executable:", sys.executable)
    
    # Check versions
    print("\n" + "="*80)
    print("CHECKING PACKAGE VERSIONS")
    print("="*80)
    
    all_correct = True
    for package, expected_version in EXPECTED_VERSIONS.items():
        installed_version = get_installed_version(package)
        
        if installed_version is None:
            print(f"❌ {package}: NOT INSTALLED")
            all_correct = False
        elif installed_version == expected_version:
            print(f"✅ {package}: {installed_version}")
        else:
            print(f"⚠️  {package}: {installed_version} (expected {expected_version})")
            all_correct = False
    
    # Verify imports
    imports_ok = verify_imports()
    
    # Check critical compatibility
    print("\n" + "="*80)
    print("CHECKING CRITICAL COMPATIBILITY")
    print("="*80)
    
    try:
        import numpy
        import streamlit
        
        numpy_version = tuple(map(int, numpy.__version__.split('.')[:2]))
        print(f"NumPy version: {numpy.__version__}")
        
        if numpy_version[0] < 2:
            print("✅ NumPy < 2: OK (Streamlit compatible)")
        else:
            print("❌ NumPy >= 2: INCOMPATIBLE with Streamlit 1.28.1")
            all_correct = False
    except Exception as e:
        print(f"❌ Error checking NumPy: {str(e)}")
        all_correct = False
    
    # Summary
    print("\n" + "="*80)
    print("VERIFICATION SUMMARY")
    print("="*80)
    
    if all_correct and imports_ok:
        print("\n✅ ALL CHECKS PASSED")
        print("Your environment is ready for deployment!")
        return 0
    else:
        print("\n❌ SOME CHECKS FAILED")
        print("Please fix the issues above before deploying")
        return 1

if __name__ == "__main__":
    sys.exit(main())
