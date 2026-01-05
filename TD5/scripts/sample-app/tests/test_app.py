"""Unit tests for Lambda application - CD Pipeline v2"""

import json
import sys
import os
import pytest

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
    
    def test_health_check_v2(self):
        """Test health check returns v2"""
        event = {
            'httpMethod': 'GET',
            'rawPath': '/',
            'pathParameters': None,
            'queryStringParameters': None
        }
        response = lambda_handler(event, self.context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['status'] == 'healthy'
        assert body['version'] == '2.0.0'
        assert 'CD Pipeline Test' in body['message']
    
    def test_api_status_v2(self):
        """Test API status returns v2"""
        event = {
            'httpMethod': 'GET',
            'rawPath': '/api/status',
            'pathParameters': None,
            'queryStringParameters': None
        }
        response = lambda_handler(event, self.context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['version'] == '2.0.0'
        assert body['service'] == 'lambda-cd-pipeline'
    
    def test_name_endpoint_with_cd(self):
        """Test name endpoint mentions CD"""
        event = {
            'httpMethod': 'GET',
            'rawPath': '/name/DevOps',
            'pathParameters': {'name': 'DevOps'},
            'queryStringParameters': None
        }
        response = lambda_handler(event, self.context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'CD Pipeline API v2' in body['message']
    
    def test_info_includes_cd_features(self):
        """Test info endpoint lists CD features"""
        event = {
            'httpMethod': 'GET',
            'rawPath': '/api/info',
            'pathParameters': None,
            'queryStringParameters': None
        }
        response = lambda_handler(event, self.context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert 'continuous-delivery' in body['deployment_stage']
        assert 'Remote state management' in body['features']
        assert 'Automated plan on PR' in body['features']

    def test_health_check_explicit(self):
        """Test health check at /health"""
        event = {
            'httpMethod': 'GET',
            'rawPath': '/health',
            'pathParameters': None,
            'queryStringParameters': None
        }
        response = lambda_handler(event, self.context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['status'] == 'healthy'
    
    def test_echo_endpoint(self):
        """Test echo endpoint"""
        event = {
            'httpMethod': 'GET',
            'rawPath': '/api/echo',
            'pathParameters': None,
            'queryStringParameters': {'param1': 'value1', 'param2': 'value2'}
        }
        response = lambda_handler(event, self.context)
        
        assert response['statusCode'] == 200
        body = json.loads(response['body'])
        assert body['total_params'] == 2
    
    def test_not_found(self):
        """Test 404 response"""
        event = {
            'httpMethod': 'GET',
            'rawPath': '/nonexistent',
            'pathParameters': None,
            'queryStringParameters': None
        }
        response = lambda_handler(event, self.context)
        
        assert response['statusCode'] == 404


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
