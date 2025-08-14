"""
Simple API Black Box Testing

Clean, concise API testing using popular packages.
"""

import pytest
import requests
import responses
from faker import Faker

fake = Faker()


class TestAPIBlackBox:
    """Simple API black box tests"""
    
    def test_get_posts(self):
        """Test GET request - real API"""
        response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
        
        assert response.status_code == 200
        data = response.json()
        assert "id" in data
        assert "title" in data
        assert "body" in data
        assert data["id"] == 1
    
    @responses.activate
    def test_create_post_mock(self):
        """Test POST request - mocked API"""
        # Mock the API response
        responses.add(
            responses.POST,
            "https://jsonplaceholder.typicode.com/posts",
            json={"id": 101, "title": "Test Post", "body": "Test Body"},
            status=201
        )
        
        # Make request
        post_data = {
            "title": fake.sentence(),
            "body": fake.text(),
            "userId": fake.random_int(1, 10)
        }
        
        response = requests.post(
            "https://jsonplaceholder.typicode.com/posts",
            json=post_data
        )
        
        assert response.status_code == 201
        assert response.json()["id"] == 101
    
    def test_api_error_handling(self):
        """Test API error scenarios"""
        response = requests.get("https://jsonplaceholder.typicode.com/posts/999")
        assert response.status_code == 404
    
    def test_api_performance(self):
        """Test API response time"""
        import time
        
        start_time = time.time()
        response = requests.get("https://jsonplaceholder.typicode.com/posts/1")
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 5.0  # Should respond within 5 seconds