"""
Simple Database Testing with Factory Boy

Using SQLite (built-in) and Factory Boy for clean database testing.
"""

import pytest
import sqlite3
import tempfile
import factory
from faker import Faker

fake = Faker()


# Simple User model for testing
class User:
    def __init__(self, id=None, name=None, email=None, age=None):
        self.id = id
        self.name = name
        self.email = email
        self.age = age


# Factory for generating test users
class UserFactory(factory.Factory):
    class Meta:
        model = User
    
    name = factory.Faker('name')
    email = factory.Faker('email')
    age = factory.Faker('random_int', min=18, max=80)


class DatabaseService:
    """Simple database service for testing"""
    
    def __init__(self, db_path=None):
        if db_path is None:
            # Create a temporary file for the database
            import tempfile
            import os
            self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.db')
            self.db_path = self.temp_file.name
            self.temp_file.close()
        else:
            self.db_path = db_path
        self.setup_database()
    
    def setup_database(self):
        """Create tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL,
                        age INTEGER
                    )
                ''')
                conn.commit()
                # Verify table was created
                cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
                result = cursor.fetchone()
                if not result:
                    raise Exception("Failed to create users table")
        except Exception as e:
            print(f"Database setup error: {e}")
            raise
    
    def cleanup(self):
        """Clean up temporary database file"""
        if hasattr(self, 'temp_file') and hasattr(self, 'db_path'):
            import os
            try:
                os.unlink(self.db_path)
            except:
                pass
    
    def create_user(self, name, email, age):
        """Create a user"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                'INSERT INTO users (name, email, age) VALUES (?, ?, ?)',
                (name, email, age)
            )
            return cursor.lastrowid
    
    def get_user(self, user_id):
        """Get user by ID"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def get_all_users(self):
        """Get all users"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute('SELECT * FROM users')
            return [dict(row) for row in cursor.fetchall()]


class TestDatabaseBlackBox:
    """Simple database black box tests"""
    
    @pytest.fixture
    def db_service(self):
        """Create database service for testing"""
        service = DatabaseService()
        yield service
        service.cleanup()
    
    def test_create_user_with_factory(self, db_service):
        """Test user creation using Factory Boy"""
        # Generate test user with Factory Boy
        test_user = UserFactory()
        
        # Create user in database
        user_id = db_service.create_user(test_user.name, test_user.email, test_user.age)
        
        # Verify user was created
        created_user = db_service.get_user(user_id)
        assert created_user is not None
        assert created_user['name'] == test_user.name
        assert created_user['email'] == test_user.email
        assert created_user['age'] == test_user.age
    
    def test_create_multiple_users(self, db_service):
        """Test creating multiple users with unique data"""
        # Create 5 users with Factory Boy
        users = UserFactory.build_batch(5)
        
        created_ids = []
        for user in users:
            user_id = db_service.create_user(user.name, user.email, user.age)
            created_ids.append(user_id)
        
        # Verify all users were created
        all_users = db_service.get_all_users()
        assert len(all_users) == 5
        
        # Verify all emails are unique
        emails = [user['email'] for user in all_users]
        assert len(set(emails)) == 5
    
    def test_user_not_found(self, db_service):
        """Test querying non-existent user"""
        user = db_service.get_user(999)
        assert user is None
    
    def test_duplicate_email_handling(self, db_service):
        """Test duplicate email constraint"""
        test_user = UserFactory()
        
        # Create first user
        db_service.create_user(test_user.name, test_user.email, test_user.age)
        
        # Try to create user with same email
        with pytest.raises(sqlite3.IntegrityError):
            db_service.create_user("Different Name", test_user.email, 25)