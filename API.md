# API Reference

Complete API documentation for the Agent Marketplace backend.

## Base URL

- Development: `http://localhost:8000`
- Production: `https://your-domain.com`

## Authentication

Most endpoints require authentication using JWT tokens.

### Getting a Token

1. Register or login to get an access token
2. Include the token in the `Authorization` header:
   ```
   Authorization: Bearer <your-token>
   ```

## Endpoints

### Authentication

#### POST /auth/register
Register a new user account.

**Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword",
  "full_name": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_admin": false,
  "created_at": "2024-01-01T00:00:00"
}
```

#### POST /auth/login
Login and receive a JWT token.

**Request Body (form-data):**
```
username: johndoe
password: securepassword
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### GET /auth/me
Get current user information.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "full_name": "John Doe",
  "is_active": true,
  "is_admin": false,
  "created_at": "2024-01-01T00:00:00"
}
```

---

### Agents

#### GET /agents/
List all public agents with optional filtering.

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Maximum records to return (default: 100)
- `search` (string): Search in name and description
- `tags` (string): Filter by tags (comma-separated)

**Example:**
```
GET /agents/?search=text&tags=nlp,processing&limit=10
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Text Reverser",
    "description": "Reverses any input text",
    "code": "text = input_data.get('text', '')\nresult = text[::-1]",
    "tags": "text,processing",
    "creator_id": 1,
    "parent_id": null,
    "version": "1.0.0",
    "is_public": true,
    "is_active": true,
    "usage_count": 42,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00",
    "average_rating": 4.5,
    "creator_username": "johndoe"
  }
]
```

#### GET /agents/{id}
Get detailed information about a specific agent.

**Response:**
```json
{
  "id": 1,
  "name": "Text Reverser",
  "description": "Reverses any input text",
  "code": "text = input_data.get('text', '')\nresult = text[::-1]",
  "tags": "text,processing",
  "creator_id": 1,
  "parent_id": null,
  "version": "1.0.0",
  "is_public": true,
  "is_active": true,
  "usage_count": 42,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00",
  "average_rating": 4.5,
  "creator_username": "johndoe"
}
```

#### POST /agents/
Create a new agent.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "name": "Text Reverser",
  "description": "Reverses any input text",
  "code": "text = input_data.get('text', '')\nresult = text[::-1]",
  "tags": "text,processing",
  "is_public": true
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "name": "Text Reverser",
  ...
}
```

#### PUT /agents/{id}
Update an existing agent (only creator or admin).

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body (all fields optional):**
```json
{
  "name": "Updated Name",
  "description": "Updated description",
  "code": "updated code",
  "tags": "new,tags",
  "is_public": true,
  "version": "1.1.0"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Updated Name",
  ...
}
```

#### DELETE /agents/{id}
Delete (soft delete) an agent (only creator or admin).

**Headers:**
```
Authorization: Bearer <token>
```

**Response (204 No Content)**

#### POST /agents/{id}/fork
Create a fork of an agent.

**Headers:**
```
Authorization: Bearer <token>
```

**Response:**
```json
{
  "id": 2,
  "name": "Text Reverser (Fork)",
  "parent_id": 1,
  "creator_id": 2,
  ...
}
```

#### GET /agents/my-agents
Get agents created by the current user.

**Headers:**
```
Authorization: Bearer <token>
```

**Query Parameters:**
- `skip` (int): Number of records to skip (default: 0)
- `limit` (int): Maximum records to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "name": "My Agent",
    ...
  }
]
```

#### POST /agents/execute
Execute an agent with input data.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "agent_id": 1,
  "input_data": {
    "text": "Hello World"
  }
}
```

**Response:**
```json
{
  "success": true,
  "output": "dlroW olleH",
  "error": null
}
```

**Error Response:**
```json
{
  "success": false,
  "output": null,
  "error": "NameError: name 'undefined_var' is not defined"
}
```

---

### Ratings

#### POST /api/ratings
Create or update a rating for an agent.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "agent_id": 1,
  "rating": 4.5
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "agent_id": 1,
  "user_id": 1,
  "rating": 4.5,
  "created_at": "2024-01-01T00:00:00"
}
```

#### GET /api/agents/{agent_id}/ratings
Get all ratings for an agent.

**Response:**
```json
[
  {
    "id": 1,
    "agent_id": 1,
    "user_id": 1,
    "rating": 4.5,
    "created_at": "2024-01-01T00:00:00"
  }
]
```

---

### Reviews

#### POST /api/reviews
Create a review for an agent.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "agent_id": 1,
  "comment": "This agent is amazing! Very useful."
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "agent_id": 1,
  "user_id": 1,
  "comment": "This agent is amazing! Very useful.",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00",
  "username": "johndoe"
}
```

#### GET /api/agents/{agent_id}/reviews
Get all reviews for an agent.

**Response:**
```json
[
  {
    "id": 1,
    "agent_id": 1,
    "user_id": 1,
    "comment": "This agent is amazing! Very useful.",
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00",
    "username": "johndoe"
  }
]
```

#### PUT /api/reviews/{id}
Update a review (only review creator).

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "comment": "Updated review text"
}
```

**Response:**
```json
{
  "id": 1,
  "comment": "Updated review text",
  ...
}
```

#### DELETE /api/reviews/{id}
Delete a review (only review creator or admin).

**Headers:**
```
Authorization: Bearer <token>
```

**Response (204 No Content)**

---

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid input data"
}
```

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Not enough permissions"
}
```

### 404 Not Found
```json
{
  "detail": "Agent not found"
}
```

### 422 Validation Error
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

## Rate Limits

Currently, there are no enforced rate limits in the development version. 
For production deployments, consider implementing rate limiting middleware.

## OpenAPI Documentation

Interactive API documentation is available at:
- Swagger UI: `/docs`
- ReDoc: `/redoc`
- OpenAPI JSON: `/openapi.json`
