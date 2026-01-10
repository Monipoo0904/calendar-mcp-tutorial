#!/usr/bin/env python3
"""
Test script to validate calendar MCP server functionality.
"""
import sys
from datetime import datetime

def test_ics_generation():
    """Test ICS file generation."""
    print("=" * 60)
    print("Testing ICS File Generation")
    print("=" * 60)
    
    from ics_generator import ICSGenerator
    from datetime import timedelta
    
    ics_gen = ICSGenerator()
    # Use relative date to ensure test remains valid over time
    future_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
    
    result = ics_gen.generate_ics(
        title="Test Event",
        date=future_date,
        description="Valentine's Day Event",
        start_time="18:00",
        end_time="20:00",
        timezone="UTC"
    )
    
    if result['success']:
        print(f"✓ ICS file generated successfully")
        print(f"  File: {result['file_path']}")
        print(f"  Filename: {result['filename']}")
        
        # Verify file exists
        import os
        if os.path.exists(result['file_path']):
            print(f"✓ File verified to exist")
            
            # Read and validate content
            with open(result['file_path'], 'r') as f:
                content = f.read()
                if 'BEGIN:VCALENDAR' in content and 'Test Event' in content:
                    print(f"✓ File content is valid")
                else:
                    print(f"✗ File content is invalid")
                    return False
        else:
            print(f"✗ Generated file does not exist")
            return False
    else:
        print(f"✗ ICS generation failed: {result.get('error')}")
        return False
    
    print()
    return True

def test_oauth_manager():
    """Test OAuth manager initialization."""
    print("=" * 60)
    print("Testing OAuth Manager")
    print("=" * 60)
    
    from oauth_manager import OAuthManager
    
    try:
        oauth_mgr = OAuthManager()
        print("✓ OAuthManager initialized successfully")
        
        # Test auth status checks (should return False without credentials)
        google_status = oauth_mgr.is_authenticated('google')
        microsoft_status = oauth_mgr.is_authenticated('microsoft')
        
        print(f"  Google authenticated: {google_status}")
        print(f"  Microsoft authenticated: {microsoft_status}")
        print()
        return True
    except Exception as e:
        print(f"✗ OAuthManager test failed: {e}")
        return False

def test_calendar_api():
    """Test Calendar API initialization."""
    print("=" * 60)
    print("Testing Calendar API")
    print("=" * 60)
    
    from calendar_api import CalendarAPI
    
    try:
        cal_api = CalendarAPI()
        print("✓ CalendarAPI initialized successfully")
        print()
        return True
    except Exception as e:
        print(f"✗ CalendarAPI test failed: {e}")
        return False

def test_main_imports():
    """Test that main.py can be imported."""
    print("=" * 60)
    print("Testing Main Module Imports")
    print("=" * 60)
    
    try:
        # We can't fully import main.py because it requires FastMCP
        # But we can check the syntax is valid
        import py_compile
        py_compile.compile('main.py', doraise=True)
        print("✓ main.py compiles successfully")
        print()
        return True
    except Exception as e:
        print(f"✗ main.py import failed: {e}")
        return False

def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("CALENDAR MCP SERVER - VALIDATION TESTS")
    print("=" * 60 + "\n")
    
    tests = [
        test_oauth_manager,
        test_calendar_api,
        test_ics_generation,
        test_main_imports,
    ]
    
    results = []
    for test_func in tests:
        try:
            result = test_func()
            results.append(result)
        except Exception as e:
            print(f"✗ Test {test_func.__name__} crashed: {e}")
            results.append(False)
    
    # Print summary
    print("=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    passed = sum(results)
    total = len(results)
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print(f"✗ {total - passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())
