#!/usr/bin/env python3
"""
Backend Test Verification Script

This script helps you verify that all backend testing components are working correctly.
Run this before running the actual tests to ensure everything is set up properly.
"""

import sys
import subprocess
import importlib
import requests
from pathlib import Path
import sqlite3
import tempfile


def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requires Python 3.9+")
        return False


def check_required_packages():
    """Check if all required packages are installed"""
    print("\n📦 Checking required packages...")
    
    required_packages = [
        'pytest',
        'requests',
        'responses',
        'factory_boy',
        'faker',
        'coverage',
        'bandit',
        'safety'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'factory_boy':
                importlib.import_module('factory')
            else:
                importlib.import_module(package)
            print(f"✅ {package} - Installed")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + " ".join(missing_packages))
        return False
    
    return True


def check_internet_connectivity():
    """Check internet connectivity for API tests"""
    print("\n🌐 Checking internet connectivity...")
    
    try:
        response = requests.get("https://jsonplaceholder.typicode.com/posts/1", timeout=10)
        if response.status_code == 200:
            print("✅ Internet connectivity - OK")
            print("✅ JSONPlaceholder API - Accessible")
            return True
        else:
            print(f"❌ JSONPlaceholder API returned status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Internet connectivity failed: {e}")
        return False


def check_database_functionality():
    """Check SQLite database functionality"""
    print("\n🗄️  Checking database functionality...")
    
    try:
        # Create temporary database
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
            db_path = tmp_file.name
        
        # Test database operations
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create table
        cursor.execute('''
            CREATE TABLE test_table (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT
            )
        ''')
        
        # Insert data
        cursor.execute("INSERT INTO test_table (name, email) VALUES (?, ?)", 
                      ("Test User", "test@example.com"))
        
        # Query data
        cursor.execute("SELECT * FROM test_table WHERE id = 1")
        result = cursor.fetchone()
        
        conn.commit()
        conn.close()
        
        # Clean up
        Path(db_path).unlink()
        
        if result and result[1] == "Test User":
            print("✅ SQLite database - Working")
            return True
        else:
            print("❌ SQLite database - Data retrieval failed")
            return False
            
    except Exception as e:
        print(f"❌ SQLite database error: {e}")
        return False


def check_test_files_exist():
    """Check if all test files exist"""
    print("\n📁 Checking test files...")
    
    test_files = [
        "backend/blackbox/test_api_simple.py",
        "backend/blackbox/test_database_simple.py", 
        "backend/whitebox/test_unit_simple.py",
        "backend/test_integration_simple.py"
    ]
    
    base_path = Path(__file__).parent
    all_exist = True
    
    for test_file in test_files:
        file_path = base_path / test_file
        if file_path.exists():
            print(f"✅ {test_file} - Exists")
        else:
            print(f"❌ {test_file} - Missing")
            all_exist = False
    
    return all_exist


def run_syntax_check():
    """Check Python syntax of test files"""
    print("\n🔍 Checking Python syntax...")
    
    test_files = [
        "backend/blackbox/test_api_simple.py",
        "backend/blackbox/test_database_simple.py",
        "backend/whitebox/test_unit_simple.py", 
        "backend/test_integration_simple.py"
    ]
    
    all_valid = True
    
    for test_file in test_files:
        try:
            with open(test_file, 'r') as f:
                compile(f.read(), test_file, 'exec')
            print(f"✅ {test_file} - Syntax OK")
        except SyntaxError as e:
            print(f"❌ {test_file} - Syntax Error: {e}")
            all_valid = False
        except FileNotFoundError:
            print(f"❌ {test_file} - File not found")
            all_valid = False
    
    return all_valid


def run_quick_test():
    """Run a quick test to verify pytest is working"""
    print("\n🧪 Running quick pytest verification...")
    
    try:
        # Run pytest with collection only (no actual test execution)
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "backend/", 
            "--collect-only", 
            "-q"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Pytest collection - OK")
            print(f"📊 Found tests in output:\n{result.stdout}")
            return True
        else:
            print(f"❌ Pytest collection failed:\n{result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Pytest collection - Timeout")
        return False
    except Exception as e:
        print(f"❌ Pytest collection error: {e}")
        return False


def run_sample_backend_test():
    """Run one simple backend test to verify functionality"""
    print("\n🎯 Running sample backend test...")
    
    try:
        # Run a single simple test
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "backend/blackbox/test_api_simple.py::TestAPIBlackBox::test_get_posts",
            "-v", "--tb=short"
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Sample backend test - PASSED")
            print("🎉 Backend testing is working correctly!")
            return True
        else:
            print(f"❌ Sample backend test - FAILED")
            print(f"Error output:\n{result.stdout}\n{result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Sample test - Timeout")
        return False
    except Exception as e:
        print(f"❌ Sample test error: {e}")
        return False


def main():
    """Main verification function"""
    print("🔍 Backend Testing Verification")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Required Packages", check_required_packages),
        ("Internet Connectivity", check_internet_connectivity),
        ("Database Functionality", check_database_functionality),
        ("Test Files", check_test_files_exist),
        ("Python Syntax", run_syntax_check),
        ("Pytest Collection", run_quick_test),
        ("Sample Test", run_sample_backend_test)
    ]
    
    passed_checks = 0
    total_checks = len(checks)
    
    for check_name, check_function in checks:
        try:
            if check_function():
                passed_checks += 1
        except Exception as e:
            print(f"❌ {check_name} - Unexpected error: {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 VERIFICATION SUMMARY")
    print(f"Passed: {passed_checks}/{total_checks} checks")
    
    if passed_checks == total_checks:
        print("🎉 ALL CHECKS PASSED! Backend testing is ready to use.")
        print("\n🚀 You can now run:")
        print("   python run_backend_tests.py --all")
        print("   pytest backend/ -v")
        return True
    else:
        print(f"⚠️  {total_checks - passed_checks} checks failed. Please fix the issues above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)