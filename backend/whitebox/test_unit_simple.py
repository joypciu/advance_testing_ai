"""
Simple White Box Unit Testing

Clean unit tests with mocking and coverage analysis.
"""

import pytest
from unittest.mock import Mock, patch
import requests


class UserService:
    """Simple user service for testing"""
    
    def __init__(self, api_url="https://api.example.com"):
        self.api_url = api_url
        self.cache = {}
    
    def get_user(self, user_id):
        """Get user from API with caching"""
        # Check cache first
        if user_id in self.cache:
            return self.cache[user_id]
        
        # Make API call
        response = requests.get(f"{self.api_url}/users/{user_id}")
        if response.status_code == 200:
            user_data = response.json()
            self.cache[user_id] = user_data
            return user_data
        
        return None
    
    def create_user(self, user_data):
        """Create user via API"""
        if not user_data.get('name') or not user_data.get('email'):
            raise ValueError("Name and email are required")
        
        response = requests.post(f"{self.api_url}/users", json=user_data)
        if response.status_code == 201:
            return response.json()
        
        raise Exception("Failed to create user")
    
    def clear_cache(self):
        """Clear user cache"""
        self.cache.clear()


class TestUserServiceWhiteBox:
    """White box tests for UserService"""
    
    @pytest.fixture
    def user_service(self):
        """Create user service instance"""
        return UserService()
    
    @patch('requests.get')
    def test_get_user_success(self, mock_get, user_service):
        """Test successful user retrieval"""
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1, "name": "John Doe"}
        mock_get.return_value = mock_response
        
        # Test the method
        result = user_service.get_user(1)
        
        # Verify results
        assert result == {"id": 1, "name": "John Doe"}
        mock_get.assert_called_once_with("https://api.example.com/users/1")
    
    @patch('requests.get')
    def test_get_user_not_found(self, mock_get, user_service):
        """Test user not found scenario"""
        # Mock 404 response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # Test the method
        result = user_service.get_user(999)
        
        # Verify results
        assert result is None
        mock_get.assert_called_once_with("https://api.example.com/users/999")
    
    @patch('requests.get')
    def test_user_caching(self, mock_get, user_service):
        """Test that users are cached properly"""
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"id": 1, "name": "John Doe"}
        mock_get.return_value = mock_response
        
        # Call twice
        result1 = user_service.get_user(1)
        result2 = user_service.get_user(1)
        
        # Verify API called only once (second call uses cache)
        assert result1 == result2
        mock_get.assert_called_once()
        
        # Verify cache contains the user
        assert 1 in user_service.cache
    
    @patch('requests.post')
    def test_create_user_success(self, mock_post, user_service):
        """Test successful user creation"""
        # Mock API response
        mock_response = Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"id": 2, "name": "Jane Doe", "email": "jane@example.com"}
        mock_post.return_value = mock_response
        
        # Test data
        user_data = {"name": "Jane Doe", "email": "jane@example.com"}
        
        # Test the method
        result = user_service.create_user(user_data)
        
        # Verify results
        assert result["id"] == 2
        assert result["name"] == "Jane Doe"
        mock_post.assert_called_once_with("https://api.example.com/users", json=user_data)
    
    def test_create_user_validation(self, user_service):
        """Test user creation validation"""
        # Test missing name
        with pytest.raises(ValueError, match="Name and email are required"):
            user_service.create_user({"email": "test@example.com"})
        
        # Test missing email
        with pytest.raises(ValueError, match="Name and email are required"):
            user_service.create_user({"name": "Test User"})
    
    @patch('requests.post')
    def test_create_user_api_failure(self, mock_post, user_service):
        """Test user creation API failure"""
        # Mock API failure
        mock_response = Mock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response
        
        user_data = {"name": "Test User", "email": "test@example.com"}
        
        # Test the method
        with pytest.raises(Exception, match="Failed to create user"):
            user_service.create_user(user_data)
    
    def test_clear_cache(self, user_service):
        """Test cache clearing functionality"""
        # Add something to cache
        user_service.cache[1] = {"id": 1, "name": "Test"}
        assert len(user_service.cache) == 1
        
        # Clear cache
        user_service.clear_cache()
        assert len(user_service.cache) == 0


# Simple calculator for coverage testing
class Calculator:
    """Simple calculator for demonstrating code coverage"""
    
    def add(self, a, b):
        return a + b
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
    
    def is_positive(self, number):
        if number > 0:
            return True
        else:
            return False


class TestCalculatorCoverage:
    """Tests to demonstrate code coverage"""
    
    @pytest.fixture
    def calculator(self):
        return Calculator()
    
    def test_add(self, calculator):
        """Test addition - covers add method"""
        assert calculator.add(2, 3) == 5
        assert calculator.add(-1, 1) == 0
    
    def test_divide_success(self, calculator):
        """Test successful division"""
        assert calculator.divide(10, 2) == 5
        assert calculator.divide(7, 2) == 3.5
    
    def test_divide_by_zero(self, calculator):
        """Test division by zero - covers error path"""
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            calculator.divide(10, 0)
    
    def test_is_positive_true(self, calculator):
        """Test positive number - covers True branch"""
        assert calculator.is_positive(5) == True
        assert calculator.is_positive(0.1) == True
    
    def test_is_positive_false(self, calculator):
        """Test non-positive number - covers False branch"""
        assert calculator.is_positive(-5) == False
        assert calculator.is_positive(0) == False