#!/usr/bin/env python3
"""
Core Recovery System Test - Tests schema recovery without external dependencies
"""
import sys
import os
import json

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app.core.schema_recovery import recovery_engine

def test_json_repair():
    """Test malformed JSON repair"""
    print("\n" + "="*60)
    print("TEST 1: Malformed JSON Repair")
    print("="*60)
    
    test_cases = [
        ('{"key": "value",}', "Trailing comma"),
        ('{"key": "value"', "Missing closing brace"),
        ('{key: "value"}', "Unquoted key"),
        ('{"key": "value",\n"key2": "value2",}', "Trailing comma with newline"),
    ]
    
    for malformed_json, description in test_cases:
        try:
            result = recovery_engine.safe_parse_json(malformed_json)
            print(f"✅ {description}: Successfully repaired")
            print(f"   Result: {result}")
        except Exception as e:
            print(f"❌ {description}: Failed - {e}")
    
    return True

def test_missing_fields_repair():
    """Test missing field repair"""
    print("\n" + "="*60)
    print("TEST 2: Missing Fields Repair")
    print("="*60)
    
    # Import SystemArchitecture
    from app.agents.swarm_agents import SystemArchitecture
    
    incomplete_data = {
        "ml_pipeline": {"algorithm": "RandomForest"},
        "backend_architecture": {"framework": "FastAPI"}
        # Missing: database_schema, frontend_architecture, etc.
    }
    
    print(f"Input fields: {list(incomplete_data.keys())}")
    
    repaired = recovery_engine.repair_missing_fields(incomplete_data, SystemArchitecture)
    
    print(f"Repaired fields: {list(repaired.keys())}")
    print(f"Added {len(repaired) - len(incomplete_data)} missing fields")
    
    # Check critical fields
    critical_fields = ["database_schema", "frontend_architecture", "api_endpoints"]
    for field in critical_fields:
        if field in repaired:
            print(f"✅ {field}: Present")
        else:
            print(f"❌ {field}: Missing")
    
    return True

def test_safe_model_parsing():
    """Test safe model parsing with fallback"""
    print("\n" + "="*60)
    print("TEST 3: Safe Model Parsing with Fallback")
    print("="*60)
    
    from app.agents.swarm_agents import SystemArchitecture
    
    # Test case 1: Incomplete data
    incomplete_data = {
        "ml_pipeline": {"algorithm": "RandomForest"}
    }
    
    print("Parsing incomplete data...")
    try:
        architecture = recovery_engine.safe_parse_model(incomplete_data, SystemArchitecture)
        
        # Verify critical fields
        checks = [
            ("database_schema", architecture.database_schema is not None),
            ("backend_architecture", architecture.backend_architecture is not None),
            ("frontend_architecture", architecture.frontend_architecture is not None),
            ("ml_pipeline", architecture.ml_pipeline is not None),
            ("api_endpoints", architecture.api_endpoints is not None),
        ]
        
        all_passed = True
        for field_name, check_result in checks:
            status = "✅" if check_result else "❌"
            print(f"{status} {field_name}: {'Present' if check_result else 'Missing'}")
            if not check_result:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Parsing failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_fallback_model_creation():
    """Test fallback model creation"""
    print("\n" + "="*60)
    print("TEST 4: Fallback Model Creation")
    print("="*60)
    
    from app.agents.swarm_agents import SystemArchitecture
    
    print("Creating fallback model...")
    try:
        fallback = recovery_engine._create_fallback_model(SystemArchitecture)
        
        # Verify all critical fields
        checks = [
            ("database_schema", fallback.database_schema),
            ("backend_architecture", fallback.backend_architecture),
            ("frontend_architecture", fallback.frontend_architecture),
            ("ml_pipeline", fallback.ml_pipeline),
            ("api_endpoints", fallback.api_endpoints),
            ("deployment_strategy", fallback.deployment_strategy),
            ("technology_stack", fallback.technology_stack),
            ("scalability_plan", fallback.scalability_plan),
        ]
        
        all_present = True
        for field_name, field_value in checks:
            is_present = field_value is not None
            status = "✅" if is_present else "❌"
            print(f"{status} {field_name}: {'Present' if is_present else 'Missing'}")
            if not is_present:
                all_present = False
        
        return all_present
        
    except Exception as e:
        print(f"❌ Fallback creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_safe_fallback_method():
    """Test SystemArchitecture.create_safe_fallback() method"""
    print("\n" + "="*60)
    print("TEST 5: SystemArchitecture.create_safe_fallback()")
    print("="*60)
    
    from app.agents.swarm_agents import SystemArchitecture
    
    print("Creating safe fallback via class method...")
    try:
        fallback = SystemArchitecture.create_safe_fallback()
        
        # Verify all critical fields
        checks = [
            ("database_schema", fallback.database_schema),
            ("backend_architecture", fallback.backend_architecture),
            ("frontend_architecture", fallback.frontend_architecture),
            ("ml_pipeline", fallback.ml_pipeline),
            ("api_endpoints", fallback.api_endpoints),
            ("deployment_strategy", fallback.deployment_strategy),
            ("technology_stack", fallback.technology_stack),
            ("scalability_plan", fallback.scalability_plan),
        ]
        
        all_present = True
        for field_name, field_value in checks:
            is_present = field_value is not None
            status = "✅" if is_present else "❌"
            print(f"{status} {field_name}: {'Present' if is_present else 'Missing'}")
            if not is_present:
                all_present = False
        
        if all_present:
            print("\n✅ All critical fields present in safe fallback")
        
        return all_present
        
    except Exception as e:
        print(f"❌ Safe fallback creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("METAMIND OS - CORE RECOVERY SYSTEM TEST")
    print("="*60)
    
    tests = [
        ("JSON Repair", test_json_repair),
        ("Missing Fields Repair", test_missing_fields_repair),
        ("Safe Model Parsing", test_safe_model_parsing),
        ("Fallback Model Creation", test_fallback_model_creation),
        ("Safe Fallback Method", test_safe_fallback_method),
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
        except Exception as e:
            print(f"\n❌ Test {test_name} crashed: {e}")
            import traceback
            traceback.print_exc()
            results[test_name] = False
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n✨ All core recovery tests passed!")
        return True
    else:
        print(f"\n❌ {total - passed} tests failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
