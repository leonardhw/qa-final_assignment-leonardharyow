#!/usr/bin/env python3
"""
Test runner script for POS Automation Test Suite
"""

import os
import sys
import subprocess
from datetime import datetime

def run_all_tests():
    """Run all test cases"""
    print("=" * 60)
    print("POS AUTOMATION TEST SUITE - ALL TESTS")
    print("=" * 60)
    print(f"Test execution started at: {datetime.now()}")
    print()
    
    # Create reports directory if it doesn't exist
    reports_dir = "reports"
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    # Define pytest command for all tests
    cmd = [
        "python", "-m", "pytest", 
        "tests/",
        "--html=reports/test_report.html",
        "--self-contained-html",
        "--tb=short",
        "-v",
        "--capture=no"
    ]
    
    try:
        # Run tests
        result = subprocess.run(cmd, cwd=os.path.dirname(__file__))
        
        print()
        print("=" * 60)
        print(f"Test execution completed at: {datetime.now()}")
        print(f"Exit code: {result.returncode}")
        print("=" * 60)
        
        if result.returncode == 0:
            print("✅ All tests PASSED!")
        else:
            print("❌ Some tests FAILED!")
            
        print(f"📊 Detailed report: {os.path.abspath('reports/test_report.html')}")
        
        return result.returncode
        
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)