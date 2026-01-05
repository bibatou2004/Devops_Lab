# API Documentation

## Overview

Full REST API documentation for the DevOps Final Project Backend.

## Base URL

```
http://localhost:8000
```

## Endpoints

### Health Check

#### Get Health Status
```http
GET /health
```

**Description**: Check if the service is running and database is connected

**Response**: `200 OK`
```json
{
  "status": "healthy",
  "service": "backend",
  "database": "connected"
}
```

---

### Tasks

#### List All Tasks
```http
GET /tasks
```

**Description**: Retrieve all tasks

**Query Parameters**: None

**Response**: `200 OK`
```json
[
  {
    "id": 1,
    "title": "Task 1",
    "description": "Description",
    "completed": false,
    "created_at": "2024-12-06T10:00:00",
    "updated_at": "2024-12-06T10:00:00"
  }
]
```

**cURL Example**:
```bash
curl http://localhost:8000/tasks
```

---

#### Get Single Task
```http
GET /tasks/{task_id}
```

**Path Parameters**:
- `task_id` (integer): Task ID

**Response**: `200 OK` or `404 Not Found`
```json
{
  "id": 1,
  "title": "Task 1",
  "description": "Description",
  "completed": false,
  "created_at": "2024-12-06T10:00:00",
  "updated_at": "2024-12-06T10:00:00"
}
```

**cURL Example**:
```bash
curl http://localhost:8000/tasks/1
```

---

#### Create Task
```http
POST /tasks
```

**Request Body**:
```json
{
  "title": "New Task",
  "description": "Task description (optional)"
}
```

**Response**: `200 OK`
```json
{
  "id": 5,
  "title": "New Task",
  "description": "Task description",
  "completed": false,
  "created_at": "2024-12-06T11:00:00",
  "updated_at": "2024-12-06T11:00:00"
}
```

**cURL Example**:
```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{
    "title": "New Task",
    "description": "Description"
  }'
```

---

#### Update Task
```http
PUT /tasks/{task_id}
```

**Path Parameters**:
- `task_id` (integer): Task ID

**Request Body** (all optional):
```json
{
  "title": "Updated Title",
  "description": "Updated description",
  "completed": true
}
```

**Response**: `200 OK`
```json
{
  "id": 1,
  "title": "Updated Title",
  "description": "Updated description",
  "completed": true,
  "created_at": "2024-12-06T10:00:00",
  "updated_at": "2024-12-06T11:30:00"
}
```

**cURL Example**:
```bash
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

---

#### Delete Task
```http
DELETE /tasks/{task_id}
```

**Path Parameters**:
- `task_id` (integer): Task ID

**Response**: `200 OK`
```json
{
  "message": "Task deleted successfully"
}
```

**cURL Example**:
```bash
curl -X DELETE http://localhost:8000/tasks/1
```

---

### Statistics

#### Get Statistics
```http
GET /stats
```

**Description**: Get aggregated statistics about all tasks

**Response**: `200 OK`
```json
{
  "total_tasks": 10,
  "completed_tasks": 3,
  "pending_tasks": 7,
  "completion_rate": 30.0
}
```

**cURL Example**:
```bash
curl http://localhost:8000/stats
```

---

## Error Responses

### 404 Not Found
```json
{
  "detail": "Task not found"
}
```

### 400 Bad Request
```json
{
  "detail": "Invalid request"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Internal server error"
}
```

---

## Testing

### Using cURL

```bash
# Health check
curl http://localhost:8000/health

# Get all tasks
curl http://localhost:8000/tasks

# Create task
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", "description": "Test task"}'

# Update task
curl -X PUT http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Delete task
curl -X DELETE http://localhost:8000/tasks/1

# Get stats
curl http://localhost:8000/stats
```

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"

# Get health
response = requests.get(f"{BASE_URL}/health")
print(response.json())

# Create task
task = {"title": "New Task", "description": "Description"}
response = requests.post(f"{BASE_URL}/tasks", json=task)
print(response.json())

# Update task
response = requests.put(f"{BASE_URL}/tasks/1", 
                        json={"completed": True})
print(response.json())

# Delete task
response = requests.delete(f"{BASE_URL}/tasks/1")
print(response.json())

# Get stats
response = requests.get(f"{BASE_URL}/stats")
print(response.json())
```

---

## Rate Limiting

Currently not implemented. Can be added using:
- FastAPI middleware
- Redis for distributed rate limiting
- Third-party services (CloudFlare, AWS WAF)

---

## Authentication

Currently no authentication. For production, add:
- JWT tokens
- OAuth 2.0
- API keys
- API Gateway authentication

---

## CORS

CORS is enabled for all origins (`*`). For production:
```python
allow_origins=["https://yourdomain.com"]
```

---

**Last Updated**: December 2024
