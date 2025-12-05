import json
from typing import Dict, Any

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for API Gateway HTTP API
    """
    path = event.get('rawPath', '/')
    method = event.get('requestContext', {}).get('http', {}).get('method', 'GET')
    query_params = event.get('queryStringParameters') or {}
    
    # Route handling
    if path == '/' or path == '/health':
        return handle_health()
    elif path == '/api/status':
        return handle_status()
    elif path.startswith('/name/'):
        name = path.split('/name/')[-1]
        return handle_name(name)
    elif path == '/api/echo':
        return handle_echo(query_params, event, context)
    elif path == '/api/info':
        return handle_info(event, context)
    else:
        return error_response(404, f"Path not found: {path}", event)


def handle_health() -> Dict[str, Any]:
    """Health check endpoint - UPDATED FOR CD TESTING"""
    return success_response({
        'status': 'healthy',
        'message': 'Lambda is running - CD Pipeline Test v2',
        'version': '2.0.0',
        'deployment_type': 'continuous-delivery'
    })


def handle_status() -> Dict[str, Any]:
    """API status endpoint"""
    return success_response({
        'status': 'operational',
        'version': '2.0.0',
        'service': 'lambda-cd-pipeline',
        'region': 'us-east-2'
    })


def handle_name(name: str) -> Dict[str, Any]:
    """Greeting endpoint with name parameter"""
    if not name or name.strip() == '':
        return error_response(400, "Name parameter is required", {})
    
    return success_response({
        'message': f'Hello {name}! Welcome to the CD Pipeline API v2',
        'name': name,
        'feature': 'continuous-delivery'
    })


def handle_echo(query_params: Dict[str, Any], event: Dict[str, Any], 
                context: Any) -> Dict[str, Any]:
    """Echo back query parameters"""
    return success_response({
        'message': 'Echo service - CD Pipeline v2',
        'query_parameters': query_params,
        'total_params': len(query_params)
    })


def handle_info(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """Application information endpoint"""
    return success_response({
        'application': 'TD5 CD Pipeline Lambda',
        'version': '2.0.0',
        'deployment_stage': 'continuous-delivery',
        'endpoints': [
            '/ or /health - Health check',
            '/api/status - API status',
            '/name/{name} - Greeting with name',
            '/api/echo?param=value - Echo parameters',
            '/api/info - This endpoint'
        ],
        'author': 'DevOps Team',
        'created': '2024',
        'features': [
            'Remote state management',
            'Automated plan on PR',
            'Automated apply on merge',
            'State locking with DynamoDB'
        ]
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
