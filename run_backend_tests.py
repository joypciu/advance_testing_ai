#!/usr/bin/env python3
"""
Simple Backend Test Runner

Clean, focused backend testing using essential packages.
Perfect for resume projects - concise yet comprehensive.
"""

import argparse
import subprocess
import sys
from pathlib import Path
import time


class BackendTestRunner:
    """Simple backend test runner"""
    
    def __init__(self):
        self.base_dir = Path(__file__).parent
        self.reports_dir = self.base_dir / "reports"
        self.reports_dir.mkdir(exist_ok=True)
    
    def run_command(self, command: list, description: str) -> bool:
        """Run a command and return success status"""
        print(f"\n{'='*50}")
        print(f"Running: {description}")
        print(f"{'='*50}")
        
        start_time = time.time()
        try:
            subprocess.run(command, check=True, cwd=self.base_dir)
            end_time = time.time()
            print(f"✅ Completed in {end_time - start_time:.2f}s")
            return True
        except subprocess.CalledProcessError:
            end_time = time.time()
            print(f"❌ Failed in {end_time - start_time:.2f}s")
            return False
    
    def run_api_tests(self) -> bool:
        """Run API black box tests"""
        command = [
            "pytest", 
            "tests/backend/blackbox/test_api_simple.py",
            "-v",
            "--html=reports/api-tests.html",
            "--self-contained-html"
        ]
        return self.run_command(command, "API Black Box Tests")
    
    def run_database_tests(self) -> bool:
        """Run database tests with Factory Boy"""
        command = [
            "pytest", 
            "tests/backend/blackbox/test_database_simple.py",
            "-v",
            "--html=reports/database-tests.html",
            "--self-contained-html"
        ]
        return self.run_command(command, "Database Tests with Factory Boy")
    
    def run_unit_tests(self) -> bool:
        """Run unit tests with mocking"""
        command = [
            "pytest", 
            "tests/backend/whitebox/test_unit_simple.py",
            "-v",
            "--cov=tests/backend/whitebox",
            "--cov-report=html:reports/coverage",
            "--html=reports/unit-tests.html",
            "--self-contained-html"
        ]
        return self.run_command(command, "Unit Tests with Coverage")
    
    def run_integration_tests(self) -> bool:
        """Run integration tests"""
        command = [
            "pytest", 
            "tests/backend/test_integration_simple.py",
            "-v",
            "--html=reports/integration-tests.html",
            "--self-contained-html"
        ]
        return self.run_command(command, "Integration Tests")
    
    def run_all_tests(self) -> bool:
        """Run all backend tests"""
        command = [
            "pytest", 
            "tests/backend/",
            "-v",
            "--cov=tests/backend",
            "--cov-report=html:reports/full-coverage",
            "--cov-report=term-missing",
            "--html=reports/all-backend-tests.html",
            "--self-contained-html"
        ]
        return self.run_command(command, "All Backend Tests")
    
    def run_security_scan(self) -> bool:
        """Run security scan"""
        commands = [
            (["bandit", "-r", "tests/backend/", "-f", "txt"], "Security Scan"),
            (["safety", "check"], "Dependency Security Check")
        ]
        
        success = True
        for command, description in commands:
            if not self.run_command(command, description):
                success = False
        return success
    
    def generate_summary(self):
        """Generate test summary"""
        print(f"\n{'='*50}")
        print("BACKEND TESTING SUMMARY")
        print(f"{'='*50}")
        
        reports = [
            ("api-tests.html", "API Tests"),
            ("database-tests.html", "Database Tests"),
            ("unit-tests.html", "Unit Tests"),
            ("integration-tests.html", "Integration Tests"),
            ("all-backend-tests.html", "Complete Test Suite")
        ]
        
        print("\n📊 Test Reports:")
        for filename, description in reports:
            filepath = self.reports_dir / filename
            status = "✅" if filepath.exists() else "❌"
            print(f"  {status} {description}: {filepath}")
        
        coverage_path = self.reports_dir / "full-coverage" / "index.html"
        if coverage_path.exists():
            print(f"\n📈 Coverage Report: {coverage_path}")
        
        print(f"\n📁 All reports: {self.reports_dir}")
        print("\n🔧 Tools Used:")
        print("  • pytest: Test framework")
        print("  • Factory Boy: Test data generation")
        print("  • Responses: HTTP mocking")
        print("  • pytest-mock: Function mocking")
        print("  • pytest-cov: Code coverage")
        print("  • Bandit: Security scanning")


def main():
    parser = argparse.ArgumentParser(description="Simple Backend Test Runner")
    
    test_group = parser.add_mutually_exclusive_group(required=True)
    test_group.add_argument("--api", action="store_true", help="Run API tests")
    test_group.add_argument("--database", action="store_true", help="Run database tests")
    test_group.add_argument("--unit", action="store_true", help="Run unit tests")
    test_group.add_argument("--integration", action="store_true", help="Run integration tests")
    test_group.add_argument("--security", action="store_true", help="Run security scan")
    test_group.add_argument("--all", action="store_true", help="Run all tests")
    
    args = parser.parse_args()
    runner = BackendTestRunner()
    
    try:
        if args.api:
            success = runner.run_api_tests()
        elif args.database:
            success = runner.run_database_tests()
        elif args.unit:
            success = runner.run_unit_tests()
        elif args.integration:
            success = runner.run_integration_tests()
        elif args.security:
            success = runner.run_security_scan()
        elif args.all:
            success = runner.run_all_tests()
        
        runner.generate_summary()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        print("\n⚠️ Test execution interrupted")
        sys.exit(130)


if __name__ == "__main__":
    main()