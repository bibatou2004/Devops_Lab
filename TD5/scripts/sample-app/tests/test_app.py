"""Unit tests for Lambda application"""

import json
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import lambda_handler


class TestLambdaHandler:
    """Test cases for lambda_handler"""
    
    def test_health_check(self):
        """Test health check endpoint"""
        event = {
            'httpMethod': 'GET',
            'path': '/health'
        }
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['status'] == 'healthy'
    
    def test_root_path(self):
        """Test root path"""
        event = {
            'httpMethod': 'GET',
            'path': '/'
        }
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['status'] == 'healthy'
    
    def test_info_endpoint(self):
        """Test info endpoint"""
        event = {
            'httpMethod': 'GET',
            'path': '/info'
        }
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['version'] == '1.0.0'
    
    def test_not_found(self):
        """Test 404 response"""
        event = {
            'httpMethod': 'GET',
            'path': '/nonexistent'
        }
        response = lambda_handler(event, None)
        
        assert response['statusCode'] == 404
        body = json.loads(response['body'])
        assert 'error' in body


if __name__ == '__main__':
    test = TestLambdaHandler()
    test.test_health_check()
    test.test_root_path()
    test.test_info_endpoint()
    test.test_not_found()
    print("✅ All tests passed!")
