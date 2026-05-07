#!/usr/bin/env python3
"""Quick deployment verification"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

print("\n=== DEPLOYMENT VERIFICATION ===\n")

# Check Python version
version = sys.version_info
print(f"[OK] Python {version.major}.{version.minor}.{version.micro}")

# Check files
files = ['app.py', 'main.py', 'document_ingestion.py', 'rag_system.py', 'utils.py', 'config.py']
for f in files:
    if os.path.exists(f):
        print(f"[OK] {f}")
    else:
        print(f"[ERROR] {f} missing")

# Check PDFs
pdfs = list(Path(".").glob("*.pdf"))
print(f"[OK] Found {len(pdfs)} PDF files")

# Check environment
env_vars = ['GEMINI_API_KEY', 'LLM_MODEL', 'LLM_PROVIDER']
for var in env_vars:
    val = os.getenv(var)
    if val:
        print(f"[OK] {var} set")
    else:
        print(f"[WARN] {var} not set")

# Check imports
print("\nChecking imports...")
try:
    import fastapi
    print("[OK] fastapi")
except:
    print("[ERROR] fastapi")

try:
    import streamlit
    print("[OK] streamlit")
except:
    print("[ERROR] streamlit")

try:
    import langchain
    print("[OK] langchain")
except:
    print("[ERROR] langchain")

try:
    import chromadb
    print("[OK] chromadb")
except:
    print("[ERROR] chromadb")

try:
    import sentence_transformers
    print("[OK] sentence_transformers")
except:
    print("[ERROR] sentence_transformers")

print("\n=== VERIFICATION COMPLETE ===\n")
