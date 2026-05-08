#!/usr/bin/env python3
"""
Test script to verify individual agent functionality
"""
import asyncio
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("backend/.env")

from backend.app.agents.analyst import AnalystAgent
from backend.app.agents.architect import ArchitectAgent
from backend.app.agents.engineer import EngineerAgent

async def test_agents():
    print("🧪 Testing Individual Agents...")
    print("=" * 50)
    
    # Load test data
    df = pd.read_csv("data/students_performance.csv")
    print(f"✅ Loaded dataset: {df.shape}")
    
    # Test Analyst
    print("\n🔍 Testing Analyst Agent...")
    analyst = AnalystAgent()
    analysis = await analyst.analyze_dataset(df, "Predict student performance")
    print(f"✅ Analysis complete: {analysis.problem_type}")
    print(f"   Target: {analysis.target_column}")
    print(f"   Features: {len(analysis.features)}")
    
    # Test Architect
    print("\n🏗️ Testing Architect Agent...")
    architect = ArchitectAgent()
    plan = await architect.design_pipeline(analysis)
    print(f"✅ Architecture designed: {len(plan.models)} models")
    print(f"   Pipeline steps: {len(plan.pipeline_steps)}")
    
    # Test Engineer
    print("\n⚙️ Testing Engineer Agent...")
    engineer = EngineerAgent()
    code_obj = await engineer.generate_code(analysis, plan, "data/students_performance.csv")
    print(f"✅ Code generated: {len(code_obj.python_code)} characters")
    print(f"   First 200 chars: {code_obj.python_code[:200]}...")
    
    # Save generated code for inspection
    with open("test_generated_code.py", "w") as f:
        f.write(code_obj.python_code)
    print("✅ Code saved to test_generated_code.py")

if __name__ == "__main__":
    asyncio.run(test_agents())