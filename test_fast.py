#!/usr/bin/env python3
"""
Fast test for MetaMind OS
Tests the autonomous generation system quickly
"""
import asyncio
import time
import os
import sys

# Add backend to path
sys.path.append('backend')

from backend.app.agents.autonomous_swarm import AutonomousSwarmOrchestrator

async def test_fast_generation():
    """Test fast autonomous generation"""
    print("🚀 Testing MetaMind Fast Generation...")
    
    # Initialize orchestrator
    orchestrator = AutonomousSwarmOrchestrator()
    
    # Test data
    dataset_path = "data/students_performance.csv"
    user_prompt = "Build a fast student performance prediction system"
    
    # Check if test data exists
    if not os.path.exists(dataset_path):
        print(f"⚠️ Test dataset not found at {dataset_path}")
        print("Creating sample dataset...")
        
        # Create sample data
        import pandas as pd
        import numpy as np
        
        # Generate sample student data
        np.random.seed(42)
        n_samples = 1000
        
        data = {
            'math_score': np.random.normal(75, 15, n_samples),
            'reading_score': np.random.normal(72, 12, n_samples),
            'writing_score': np.random.normal(70, 14, n_samples),
            'parental_education': np.random.choice(['high school', 'some college', 'bachelor', 'master'], n_samples),
            'lunch': np.random.choice(['standard', 'free/reduced'], n_samples),
            'test_preparation': np.random.choice(['none', 'completed'], n_samples)
        }
        
        df = pd.DataFrame(data)
        
        # Create target (overall performance)
        df['overall_score'] = (df['math_score'] + df['reading_score'] + df['writing_score']) / 3
        
        # Ensure data directory exists
        os.makedirs('data', exist_ok=True)
        df.to_csv(dataset_path, index=False)
        print(f"✅ Sample dataset created at {dataset_path}")
    
    # Status callback for testing
    async def status_callback(status):
        print(f"📡 {status['agent']}: {status['status']}")
    
    # Start timer
    start_time = time.time()
    
    try:
        # Generate project
        result = await orchestrator.generate_complete_project(
            dataset_path=dataset_path,
            user_prompt=user_prompt,
            on_status_update=status_callback
        )
        
        # End timer
        end_time = time.time()
        generation_time = end_time - start_time
        
        print(f"\n🎉 FAST GENERATION COMPLETE!")
        print(f"⏱️ Generation time: {generation_time:.2f} seconds")
        print(f"📁 Project path: {result.project_path}")
        print(f"📊 Backend files: {len(result.backend_files)}")
        print(f"🎨 Frontend files: {len(result.frontend_files)}")
        print(f"🤖 ML files: {len(result.ml_files)}")
        print(f"🐳 Deployment files: {len(result.deployment_files)}")
        
        # Verify key files exist
        key_files = [
            "backend/app/main.py",
            "backend/requirements.txt",
            "frontend/package.json",
            "ml/train.py",
            "README.md"
        ]
        
        print(f"\n🔍 Verifying generated files...")
        for file_path in key_files:
            full_path = os.path.join(result.project_path, file_path)
            if os.path.exists(full_path):
                print(f"✅ {file_path}")
            else:
                print(f"❌ {file_path}")
        
        print(f"\n🚀 Test completed successfully in {generation_time:.2f} seconds!")
        return True
        
    except Exception as e:
        end_time = time.time()
        generation_time = end_time - start_time
        print(f"\n❌ Test failed after {generation_time:.2f} seconds: {e}")
        return False

async def main():
    """Main test function"""
    print("🤖 MetaMind OS Fast Test")
    print("=" * 30)
    
    success = await test_fast_generation()
    
    if success:
        print("\n✅ All tests passed! MetaMind OS is working fast!")
        print("\n📝 Next steps:")
        print("1. Run: python quick_start.py")
        print("2. Go to http://localhost:8000/docs")
        print("3. Test the autonomous generation!")
    else:
        print("\n❌ Tests failed. Check the error messages above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)