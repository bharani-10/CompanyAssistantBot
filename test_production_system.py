#!/usr/bin/env python3
"""
Production-Grade MetaMind OS Test Suite
Tests the complete autonomous generation pipeline with real validation
"""
import asyncio
import os
import sys
import json
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.mission_state import mission_manager, MissionPhase
from app.core.schema_recovery import recovery_engine
from app.agents.swarm_agents import (
    AnalystAgent, ArchitectAgent, SystemArchitecture, DatasetIntelligence
)
from app.agents.autonomous_swarm import AutonomousSwarmOrchestrator

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_header(text):
    print(f"\n{BLUE}{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}{RESET}\n")

def print_success(text):
    print(f"{GREEN}✅ {text}{RESET}")

def print_error(text):
    print(f"{RED}❌ {text}{RESET}")

def print_warning(text):
    print(f"{YELLOW}⚠️  {text}{RESET}")

def print_info(text):
    print(f"{BLUE}ℹ️  {text}{RESET}")

async def test_schema_recovery():
    """Test 1: Schema Recovery Engine"""
    print_header("TEST 1: Schema Recovery Engine")
    
    try:
        # Test 1a: Repair missing fields
        print_info("Testing missing field repair...")
        incomplete_data = {
            "ml_pipeline": {"algorithm": "RandomForest"},
            "backend_architecture": {"framework": "FastAPI"}
            # Missing: database_schema, frontend_architecture, etc.
        }
        
        repaired = recovery_engine.repair_missing_fields(incomplete_data, SystemArchitecture)
        print_success(f"Repaired {len(repaired) - len(incomplete_data)} missing fields")
        
        # Test 1b: Safe JSON parsing
        print_info("Testing malformed JSON repair...")
        malformed_json = '{"ml_pipeline": {"algorithm": "RandomForest",}, "backend": {"framework": "FastAPI"'
        parsed = recovery_engine.safe_parse_json(malformed_json)
        print_success("Malformed JSON successfully repaired")
        
        # Test 1c: Safe model parsing with fallback
        print_info("Testing safe model parsing with fallback...")
        architecture = recovery_engine.safe_parse_model(incomplete_data, SystemArchitecture)
        
        # Verify critical fields exist
        assert architecture.database_schema is not None, "database_schema should not be None"
        assert architecture.backend_architecture is not None, "backend_architecture should not be None"
        assert architecture.ml_pipeline is not None, "ml_pipeline should not be None"
        
        print_success("Safe model parsing successful - all critical fields present")
        
        # Test 1d: Fallback model creation
        print_info("Testing fallback model creation...")
        fallback = recovery_engine._create_fallback_model(SystemArchitecture)
        assert fallback.database_schema is not None, "Fallback should have database_schema"
        print_success("Fallback model creation successful")
        
        return True
        
    except Exception as e:
        print_error(f"Schema recovery test failed: {e}")
        return False

async def test_dataset_analysis():
    """Test 2: Dataset Analysis"""
    print_header("TEST 2: Dataset Analysis")
    
    try:
        # Create test dataset
        print_info("Creating test dataset...")
        test_data = {
            'feature_1': np.random.randn(100),
            'feature_2': np.random.randn(100),
            'feature_3': np.random.choice(['A', 'B', 'C'], 100),
            'target': np.random.randint(0, 2, 100)
        }
        df = pd.DataFrame(test_data)
        dataset_path = "test_dataset.csv"
        df.to_csv(dataset_path, index=False)
        print_success(f"Test dataset created: {dataset_path}")
        
        # Analyze dataset
        print_info("Analyzing dataset...")
        analyst = AnalystAgent()
        analysis = await analyst.analyze_dataset_intelligence(
            dataset_path,
            "Predict target column using classification"
        )
        
        # Verify analysis
        assert analysis.problem_type in ['classification', 'regression', 'clustering'], "Invalid problem type"
        assert analysis.target_column is not None, "Target column not detected"
        assert len(analysis.features) > 0, "No features detected"
        assert analysis.data_quality_score > 0, "Invalid data quality score"
        
        print_success(f"Dataset analysis successful:")
        print(f"  - Problem type: {analysis.problem_type}")
        print(f"  - Target column: {analysis.target_column}")
        print(f"  - Features: {len(analysis.features)}")
        print(f"  - Data quality: {analysis.data_quality_score:.2%}")
        print(f"  - Recommended algorithms: {analysis.recommended_algorithms}")
        
        # Cleanup
        os.remove(dataset_path)
        
        return True
        
    except Exception as e:
        print_error(f"Dataset analysis test failed: {e}")
        return False

async def test_architecture_generation():
    """Test 3: Architecture Generation with Recovery"""
    print_header("TEST 3: Architecture Generation with Recovery")
    
    try:
        # Create mock analysis
        print_info("Creating mock dataset analysis...")
        analysis = DatasetIntelligence(
            problem_type="classification",
            target_column="target",
            features=["feature_1", "feature_2", "feature_3"],
            categorical_features=["feature_3"],
            numerical_features=["feature_1", "feature_2"],
            dataset_size=(100, 4),
            missing_values={},
            data_quality_score=0.95,
            recommended_algorithms=["RandomForest", "LogisticRegression"],
            preprocessing_requirements=["StandardScaling", "OneHotEncoding"],
            business_context="Classification task",
            technical_complexity="medium"
        )
        
        # Generate architecture
        print_info("Generating system architecture...")
        architect = ArchitectAgent()
        architecture = await architect.design_complete_system(analysis)
        
        # Verify architecture
        assert architecture.ml_pipeline is not None, "ml_pipeline is None"
        assert architecture.backend_architecture is not None, "backend_architecture is None"
        assert architecture.frontend_architecture is not None, "frontend_architecture is None"
        assert architecture.database_schema is not None, "database_schema is None"
        assert architecture.api_endpoints is not None, "api_endpoints is None"
        assert architecture.deployment_strategy is not None, "deployment_strategy is None"
        assert architecture.technology_stack is not None, "technology_stack is None"
        assert architecture.scalability_plan is not None, "scalability_plan is None"
        
        print_success("Architecture generation successful:")
        print(f"  - ML Pipeline: {architecture.ml_pipeline.get('algorithm', 'N/A')}")
        print(f"  - Backend: {architecture.backend_architecture.get('framework', 'N/A')}")
        print(f"  - Frontend: {architecture.frontend_architecture.get('framework', 'N/A')}")
        print(f"  - Database: {architecture.database_schema.get('type', 'N/A')}")
        print(f"  - Deployment: {architecture.deployment_strategy.get('containerization', 'N/A')}")
        
        return True
        
    except Exception as e:
        print_error(f"Architecture generation test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_mission_state_management():
    """Test 4: Mission State Management"""
    print_header("TEST 4: Mission State Management")
    
    try:
        # Create mission
        print_info("Creating mission...")
        mission_id = mission_manager.create_mission(
            "test_dataset.csv",
            "Test autonomous generation"
        )
        print_success(f"Mission created: {mission_id}")
        
        # Update mission
        print_info("Updating mission state...")
        mission_manager.update_mission(mission_id,
            phase=MissionPhase.ANALYZING,
            progress=25
        )
        print_success("Mission state updated")
        
        # Add logs
        print_info("Adding mission logs...")
        mission_manager.add_log(mission_id, "Analyst", "Analyzing dataset", MissionPhase.ANALYZING)
        mission_manager.add_log(mission_id, "Architect", "Designing architecture", MissionPhase.ARCHITECTING)
        print_success("Mission logs added")
        
        # Get mission
        mission = mission_manager.get_mission(mission_id)
        assert mission is not None, "Mission not found"
        assert mission.phase == MissionPhase.ANALYZING, "Mission phase incorrect"
        assert len(mission.logs) >= 2, "Mission logs not saved"
        
        print_success(f"Mission state verified:")
        print(f"  - Phase: {mission.phase}")
        print(f"  - Progress: {mission.progress}%")
        print(f"  - Logs: {len(mission.logs)}")
        
        return True
        
    except Exception as e:
        print_error(f"Mission state management test failed: {e}")
        return False

async def test_file_counting():
    """Test 5: Real File Counting"""
    print_header("TEST 5: Real File Counting")
    
    try:
        # Create test project structure
        print_info("Creating test project structure...")
        test_project = "test_project_structure"
        os.makedirs(f"{test_project}/backend/app", exist_ok=True)
        os.makedirs(f"{test_project}/frontend/src", exist_ok=True)
        os.makedirs(f"{test_project}/ml/models", exist_ok=True)
        
        # Create test files
        test_files = [
            f"{test_project}/backend/app/main.py",
            f"{test_project}/backend/app/service.py",
            f"{test_project}/backend/requirements.txt",
            f"{test_project}/frontend/src/App.tsx",
            f"{test_project}/frontend/src/index.tsx",
            f"{test_project}/ml/models/model.pkl",
            f"{test_project}/Dockerfile",
            f"{test_project}/README.md"
        ]
        
        for file_path in test_files:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                f.write("test content")
        
        print_success(f"Created {len(test_files)} test files")
        
        # Count files
        print_info("Counting real files...")
        mission_id = mission_manager.create_mission("test.csv", "File counting test")
        counts = mission_manager.count_real_files(mission_id, test_project)
        
        assert counts["backend"] > 0, "Backend files not counted"
        assert counts["frontend"] > 0, "Frontend files not counted"
        assert counts["ml"] > 0, "ML files not counted"
        assert counts["total"] > 0, "Total files not counted"
        
        print_success(f"File counting successful:")
        print(f"  - Backend: {counts['backend']} files")
        print(f"  - Frontend: {counts['frontend']} files")
        print(f"  - ML: {counts['ml']} files")
        print(f"  - Deployment: {counts['deployment']} files")
        print(f"  - Total: {counts['total']} files")
        
        # Cleanup
        import shutil
        shutil.rmtree(test_project)
        
        return True
        
    except Exception as e:
        print_error(f"File counting test failed: {e}")
        return False

async def run_all_tests():
    """Run all production tests"""
    print_header("METAMIND OS - PRODUCTION TEST SUITE")
    print_info(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    tests = [
        ("Schema Recovery Engine", test_schema_recovery),
        ("Dataset Analysis", test_dataset_analysis),
        ("Architecture Generation", test_architecture_generation),
        ("Mission State Management", test_mission_state_management),
        ("Real File Counting", test_file_counting),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            result = await test_func()
            results[test_name] = result
        except Exception as e:
            print_error(f"Test {test_name} crashed: {e}")
            results[test_name] = False
    
    # Summary
    print_header("TEST SUMMARY")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = f"{GREEN}PASS{RESET}" if result else f"{RED}FAIL{RESET}"
        print(f"  {status} - {test_name}")
    
    print(f"\n{BLUE}Total: {passed}/{total} tests passed{RESET}")
    
    if passed == total:
        print_success("All production tests passed! ✨")
        return True
    else:
        print_error(f"{total - passed} tests failed")
        return False

if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
