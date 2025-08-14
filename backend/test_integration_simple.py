"""
Simple Backend Integration Testing

Clean integration tests combining multiple components.
"""

import pytest
import sqlite3
import requests
from unittest.mock import patch, Mock
from factory import Factory, Faker as FactoryFaker


# Simple models
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


# Simple services for integration testing
class DatabaseService:
    def __init__(self):
        self.conn = sqlite3.connect(':memory:')
        self.setup_tables()
    
    def setup_tables(self):
        self.conn.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY,
                name TEXT,
                email TEXT UNIQUE,
                age INTEGER
            )
        ''')
    
    def save_user(self, user):
        cursor = self.conn.execute(
            'INSERT INTO users (name, email, age) VALUES (?, ?, ?)',
            (user.name, user.email, user.age)
        )
        return cursor.lastrowid
    
    def get_user(self, user_id):
        cursor = self.conn.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        row = cursor.fetchone()
        return {'id': row[0], 'name': row[1], 'email': row[2], 'age': row[3]} if row else None


class NotificationService:
    def send_welcome_email(self, email, name):
        # Simulate email sending
        return f"Welcome email sent to {email} for {name}"


class UserRegistrationService:
    def __init__(self, db_service, notification_service):
        self.db_service = db_service
        self.notification_service = notification_service
    
    def register_user(self, user_data):
        # Validate user data
        if not user_data.get('name') or not user_data.get('email'):
            raise ValueError("Name and email are required")
        
        # Create user object
        user = User(user_data['name'], user_data['email'], user_data.get('age', 25))
        
        # Save to database
        user_id = self.db_service.save_user(user)
        
        # Send welcome email
        self.notification_service.send_welcome_email(user.email, user.name)
        
        # Return created user
        return self.db_service.get_user(user_id)


class TestBackendIntegration:
    """Integration tests for backend services"""
    
    @pytest.fixture
    def services(self):
        """Setup integrated services"""
        db_service = DatabaseService()
        notification_service = NotificationService()
        registration_service = UserRegistrationService(db_service, notification_service)
        
        return {
            'db': db_service,
            'notification': notification_service,
            'registration': registration_service
        }
    
    def test_user_registration_flow(self, services):
        """Test complete user registration flow"""
        # Generate test user with Factory
        test_user = UserFactory()
        user_data = {
            'name': test_user.name,
            'email': test_user.email,
            'age': test_user.age
        }
        
        # Register user
        created_user = services['registration'].register_user(user_data)
        
        # Verify user was created
        assert created_user is not None
        assert created_user['name'] == test_user.name
        assert created_user['email'] == test_user.email
        assert created_user['age'] == test_user.age
        assert 'id' in created_user
    
    def test_registration_validation(self, services):
        """Test registration validation"""
        # Test missing name
        with pytest.raises(ValueError, match="Name and email are required"):
            services['registration'].register_user({'email': 'test@example.com'})
        
        # Test missing email
        with pytest.raises(ValueError, match="Name and email are required"):
            services['registration'].register_user({'name': 'Test User'})
    
    def test_multiple_user_registration(self, services):
        """Test registering multiple users"""
        # Generate multiple test users
        users = UserFactory.build_batch(3)
        
        created_users = []
        for user in users:
            user_data = {'name': user.name, 'email': user.email, 'age': user.age}
            created_user = services['registration'].register_user(user_data)
            created_users.append(created_user)
        
        # Verify all users were created with unique IDs
        assert len(created_users) == 3
        user_ids = [user['id'] for user in created_users]
        assert len(set(user_ids)) == 3  # All unique
    
    @patch('requests.post')
    def test_external_api_integration(self, mock_post, services):
        """Test integration with external API"""
        # Mock external API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'status': 'success', 'user_id': 123}
        mock_post.return_value = mock_response
        
        # Test user data
        test_user = UserFactory()
        user_data = {'name': test_user.name, 'email': test_user.email}
        
        # Register user (this would normally call external API)
        created_user = services['registration'].register_user(user_data)
        
        # Verify user was created locally
        assert created_user['name'] == test_user.name
        assert created_user['email'] == test_user.email
    
    def test_database_transaction_rollback(self, services):
        """Test database transaction handling"""
        test_user = UserFactory()
        
        # First registration should succeed
        user_data = {'name': test_user.name, 'email': test_user.email}
        created_user = services['registration'].register_user(user_data)
        assert created_user is not None
        
        # Second registration with same email should fail
        with pytest.raises(sqlite3.IntegrityError):
            services['registration'].register_user(user_data)


class TestServicePerformance:
    """Simple performance tests"""
    
    @pytest.fixture
    def services(self):
        db_service = DatabaseService()
        notification_service = NotificationService()
        registration_service = UserRegistrationService(db_service, notification_service)
        return {'registration': registration_service}
    
    def test_bulk_user_registration_performance(self, services):
        """Test performance of bulk user registration"""
        import time
        
        # Generate test users
        users = UserFactory.build_batch(50)
        
        start_time = time.time()
        
        # Register all users
        for user in users:
            user_data = {'name': user.name, 'email': user.email, 'age': user.age}
            services['registration'].register_user(user_data)
        
        end_time = time.time()
        total_time = end_time - start_time
        
        # Assert reasonable performance (adjust threshold as needed)
        assert total_time < 5.0, f"Bulk registration too slow: {total_time:.2f}s"
        
        print(f"Registered 50 users in {total_time:.3f}s")