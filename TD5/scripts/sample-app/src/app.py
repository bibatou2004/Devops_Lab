"""
Lambda application for API Gateway integration
Supports multiple endpoints with path and query parameters
"""

import json
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Handle API Gateway requests.
    
    Args:
        event: API Gateway event with path, method, parameters
        context: Lambda context
        
    Returns:
        API Gateway response (statusCode, headers, body)
    """
    logger.info(f"Received event: {json.dumps(event)}")
    
    try:
        # Extract request information
        http_method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        path_params = event.get('pathParameters') or {}
        query_params = event.get('queryStringParameters') or {}
        
        logger.info(f"Method: {http_method}, Path: {path}, PathParams: {path_params}")
        
        # Route handlers
        if path == '/' or path == '/health':
            return handle_health(event, context)
        
        elif path == '/api/status':
            return handle_status(event, context)
        
        elif path.startswith('/name/'):
            # Extract name from path
            name = path.split('/name/')[-1]
            return handle_name(name, event, context)
        
        elif path == '/api/echo':
            # Echo back query parameters
            return handle_echo(query_params, event, context)
        
        elif path == '/api/info':
            return handle_info(event, context)
        
        else:
            return error_response(404, "Endpoint not found", event)
    
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        return error_response(500, f"Internal Server Error: {str(e)}", event)


def handle_health(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Health check endpoint"""
    return success_response({
        'status': 'healthy',
        'message': 'Lambda function is running',
        'path': event.get('path'),
        'timestamp': context.invoked_function_arn
    })


def handle_status(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """API status endpoint"""
    return success_response({
        'status': 'operational',
        'service': 'TD5 Lambda API',
        'version': '1.0.0',
        'environment': 'production',
        'request_id': context.request_id
    })


def handle_name(name: str, event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Handle /name/:name endpoint
    Returns a greeting with the provided name
    """
    if not name or name.strip() == '':
        return error_response(400, "Name parameter is required", event)
    
    return success_response({
        'message': f'Hello, {name}!',
        'name': name,
        'path': event.get('path'),
        'greeting': f'Welcome to TD5, {name}! This is your Lambda API.'
    })


def handle_echo(query_params: Dict[str, Any], event: Dict[str, Any], 
                context: Any) -> Dict[str, Any]:
    """Echo back query parameters"""
    return success_response({
        'message': 'Echo service',
        'query_parameters': query_params,
        'total_params': len(query_params)
    })


def handle_info(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Application information endpoint"""
    return success_response({
        'application': 'TD5 Sample Lambda',
        'version': '1.0.0',
        'endpoints': [
            '/ or /health - Health check',
            '/api/status - API status',
            '/name/{name} - Greeting with name',
            '/api/echo?param=value - Echo parameters',
            '/api/info - This endpoint'
        ],
        'author': 'DevOps Team',
        'created': '2024'
    })


def success_response(data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a successful API response"""
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(data, indent=2)
    }


def error_response(status_code: int, message: str, 
                   event: Dict[str, Any]) -> Dict[str, Any]:
    """Create an error API response"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'error': message,
            'status_code': status_code,
            'path': event.get('path'),
            'method': event.get('httpMethod')
        }, indent=2)
    }
