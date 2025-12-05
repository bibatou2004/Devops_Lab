"""Unit tests for Lambda application"""

import json
import sys
import os
import pytest

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from app import lambda_handler


class MockContext:
    """Mock Lambda context"""
    def __init__(self):
        self.request_id = 'test-request-id-12345'
        self.invoked_function_arn = 'arn:aws:lambda:us-east-2:123456789:function:test'


class TestLambdaHandler:
    """Test cases for lambda_handler"""
    
    def setup_method(self):
        """Setup for each test"""
        self.context = MockContext()
    
    # Health Check Tests
    def test_health_check_root(self):
        """Test health check at root path"""
        event = {
            'httpMethod': 'GET',
            'path': '/',
            'pathParameters': None,
            'queryStringParameters': None
        }
        response = lambda_handler(event, self.context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['status'] == 'healthy'
        assert 'message' in body
    
    def test_health_check_explicit(self):
        """Test health check at /health"""
        event = {
            'httpMethod': 'GET',
            'path': '/health',
            'pathParameters': None,
            'queryStringParameters': None
        }
        response = lambda_handler(event, self.context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['status'] == 'healthy'
    
    # Status Tests
    def test_api_status(self):
        """Test API status endpoint"""
        event = {
            'httpMethod': 'GET',
            'path': '/api/status',
            'pathParameters': None,
            'queryStringParameters': None
        }
        response = lambda_handler(event, self.context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['status'] == 'operational'
        assert body['version'] == '1.0.0'
    
    # Name Parameter Tests
    def test_name_endpoint_devops(self):
        """Test /name/DevOps endpoint"""
        event = {
            'httpMethod': 'GET',
            'path': '/name/DevOps',
            'pathParameters': {'name': 'DevOps'},
            'queryStringParameters': None
        }
        response = lambda_handler(event, self.context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'DevOps' in body['message']
        assert body['name'] == 'DevOps'
    
    def test_name_endpoint_biba(self):
        """Test /name/Biba endpoint"""
        event = {
            'httpMethod': 'GET',
            'path': '/name/Biba',
            'pathParameters': {'name': 'Biba'},
            'queryStringParameters': None
        }
        response = lambda_handler(event, self.context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'Biba' in body['message']
        assert body['name'] == 'Biba'
    
    def test_name_endpoint_empty(self):
        """Test /name/ with empty name"""
        event = {
            'httpMethod': 'GET',
            'path': '/name/',
            'pathParameters': {'name': ''},
            'queryStringParameters': None
        }
        response = lambda_handler(event, self.context)
        
        assert response['statusCode'] == 400
        body = json.loads(response['body'])
        assert 'error' in body
    
    # Echo Tests
    def test_echo_endpoint(self):
        """Test /api/echo endpoint"""
        event = {
            'httpMethod': 'GET',
            'path': '/api/echo',
            'pathParameters': None,
            'queryStringParameters': {'param1': 'value1', 'param2': 'value2'}
        }
        response = lambda_handler(event, self.context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['total_params'] == 2
    
    # Info Tests
    def test_info_endpoint(self):
        """Test /api/info endpoint"""
        event = {
            'httpMethod': 'GET',
            'path': '/api/info',
            'pathParameters': None,
            'queryStringParameters': None
        }
        response = lambda_handler(event, self.context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'endpoints' in body
        assert len(body['endpoints']) > 0
    
    # Error Tests
    def test_not_found(self):
        """Test 404 response for unknown path"""
        event = {
            'httpMethod': 'GET',
            'path': '/nonexistent',
            'pathParameters': None,
            'queryStringParameters': None
        }
        response = lambda_handler(event, self.context)
        
        assert response['statusCode'] == 404
        body = json.loads(response['body'])
        assert 'error' in body
    
    # Response Format Tests
    def test_response_headers(self):
        """Test response has correct headers"""
        event = {
            'httpMethod': 'GET',
            'path': '/',
            'pathParameters': None,
            'queryStringParameters': None
        }
        response = lambda_handler(event, self.context)
        
        assert 'headers' in response
        assert response['headers']['Content-Type'] == 'application/json'
        assert 'Access-Control-Allow-Origin' in response['headers']
    
    def test_response_is_valid_json(self):
        """Test all responses are valid JSON"""
        event = {
            'httpMethod': 'GET',
            'path': '/api/status',
            'pathParameters': None,
            'queryStringParameters': None
        }
        response = lambda_handler(event, self.context)
        
        # Should not raise
        body = json.loads(response['body'])
        assert isinstance(body, dict)


if __name__ == '__main__':
    # Run with pytest
    pytest.main([__file__, '-v'])
