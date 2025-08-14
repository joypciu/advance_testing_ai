#!/usr/bin/env python3
"""
Backend Testing Demo

This script demonstrates the backend testing functionality with simple examples.
"""

import requests
import sqlite3
import tempfile
from factory import Factory, Faker as FactoryFaker
from unittest.mock import Mock, patch
import responses


# Demo classes for testing
class User:
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age


class UserFactory(Factory):
    class Meta:
        model = User
    
    name = FactoryFaker('name')
    email = FactoryFaker('email')
    age = FactoryFaker('random_int', min=18, max=65)


def demo_api_testing():
    """Demonstrate API testing functionality"""
    print("🌐 API Testing Demo")
    print("-" * 30)
    
    try:
        # Real API call
        print("1. Testing real API call...")
        response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Real API call successful")
            print(f"   Post ID: {data['id']}")
            print(f"   Title: {data['title'][:50]}...")
        else:
            print(f"❌ Real API call failed: {response.status_code}")
            return False
        
        # Mocked API call
        print("\n2. Testing mocked API call...")
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.GET,
                "https://api.example.com/users/1",
                json={"id": 1, "name": "Test User", "email": "test@example.com"},
                status=200
            )
            
            mock_response = requests.get("https://api.example.com/users/1")
            if mock_response.status_code == 200:
                mock_data = mock_response.json()
                print(f"✅ Mocked API call successful")
                print(f"   User: {mock_data['name']}")
                print(f"   Email: {mock_data['email']}")
            else:
                print(f"❌ Mocked API call failed")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ API testing error: {e}")
        return False


def demo_database_testing():
    """Demonstrate database testing functionality"""
    print("\n🗄️  Database Testing Demo")
    print("-" * 30)
    
    try:
        # Create temporary database
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as tmp_file:
            db_path = tmp_file.name
        
        print("1. Creating test database...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Create table
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT UNIQUE,
                age INTEGER
            )
        ''')
        
        print("✅ Database table created")
        
        # Test data insertion
        print("\n2. Testing data insertion...")
        test_users = [
            ("John Doe", "john@example.com", 30),
            ("Jane Smith", "jane@example.com", 25),
            ("Bob Wilson", "bob@example.com", 35)
        ]
        
        for name, email, age in test_users:
            cursor.execute(
                "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                (name, email, age)
            )
        
        conn.commit()
        print(f"✅ Inserted {len(test_users)} users")
        
        # Test data retrieval
        print("\n3. Testing data retrieval...")
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        print(f"✅ Retrieved user count: {count}")
        
        cursor.execute("SELECT * FROM users WHERE age > 28")
        older_users = cursor.fetchall()
        print(f"✅ Found {len(older_users)} users over 28")
        
        # Test constraint
        print("\n4. Testing unique constraint...")
        try:
            cursor.execute(
                "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
                ("Duplicate", "john@example.com", 40)  # Duplicate email
            )
            conn.commit()
            print("❌ Unique constraint not working")
            return False
        except sqlite3.IntegrityError:
            print("✅ Unique constraint working correctly")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Database testing error: {e}")
        return False


def demo_factory_testing():
    """Demonstrate Factory Boy functionality"""
    print("\n🏭 Factory Boy Demo")
    print("-" * 30)
    
    try:
        print("1. Generating single user...")
        user = UserFactory()
        print(f"✅ Generated user: {user.name}, {user.email}, age {user.age}")
        
        print("\n2. Generating multiple users...")
        users = UserFactory.build_batch(5)
        print(f"✅ Generated {len(users)} users:")
        for i, user in enumerate(users, 1):
            print(f"   {i}. {user.name} ({user.age} years old)")
        
        # Verify all emails are unique
        emails = [user.email for user in users]
        if len(set(emails)) == len(emails):
            print("✅ All generated emails are unique")
        else:
            print("❌ Duplicate emails found")
            return False
        
        print("\n3. Generating user with custom data...")
        custom_user = UserFactory(name="Custom User", age=99)
        print(f"✅ Custom user: {custom_user.name}, age {custom_user.age}")
        
        return True
        
    except Exception as e:
        print(f"❌ Factory testing error: {e}")
        return False


def demo_mocking():
    """Demonstrate mocking functionality"""
    print("\n🎭 Mocking Demo")
    print("-" * 30)
    
    try:
        print("1. Testing function mocking...")
        
        # Create a mock function
        mock_function = Mock(return_value="mocked result")
        result = mock_function("test input")
        
        if result == "mocked result":
            print("✅ Function mocking working")
            print(f"   Mock was called with: {mock_function.call_args}")
        else:
            print("❌ Function mocking failed")
            return False
        
        print("\n2. Testing method patching...")
        
        class TestService:
            def get_data(self):
                return "real data"
        
        service = TestService()
        
        # Test without patch
        real_result = service.get_data()
        print(f"   Real method result: {real_result}")
        
        # Test with patch
        with patch.object(service, 'get_data', return_value="patched data"):
            patched_result = service.get_data()
            print(f"   Patched method result: {patched_result}")
        
        if patched_result == "patched data":
            print("✅ Method patching working")
        else:
            print("❌ Method patching failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Mocking error: {e}")
        return False


def main():
    """Run all backend testing demos"""
    print("🎯 Backend Testing Functionality Demo")
    print("=" * 50)
    
    demos = [
        ("API Testing", demo_api_testing),
        ("Database Testing", demo_database_testing),
        ("Factory Boy", demo_factory_testing),
        ("Mocking", demo_mocking)
    ]
    
    passed_demos = 0
    total_demos = len(demos)
    
    for demo_name, demo_function in demos:
        try:
            if demo_function():
                passed_demos += 1
                print(f"✅ {demo_name} demo completed successfully\n")
            else:
                print(f"❌ {demo_name} demo failed\n")
        except Exception as e:
            print(f"❌ {demo_name} demo error: {e}\n")
    
    print("=" * 50)
    print(f"📊 DEMO SUMMARY")
    print(f"Successful: {passed_demos}/{total_demos} demos")
    
    if passed_demos == total_demos:
        print("🎉 ALL DEMOS PASSED! Backend testing components are working correctly.")
        print("\n🚀 Ready to run full backend tests:")
        print("   python run_backend_tests.py --all")
    else:
        print(f"⚠️  {total_demos - passed_demos} demos failed. Check the errors above.")
    
    return passed_demos == total_demos


if __name__ == "__main__":
    main()