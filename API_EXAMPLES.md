# API Usage Examples

This document provides practical examples of using the E-Commerce API.

## Base URL
```
http://localhost:8000
```

## 1. User Registration

Register a new user account.

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "username": "johndoe",
    "password": "secretpass123"
  }'
```

**Response:**
```json
{
  "id": 1,
  "email": "john@example.com",
  "username": "johndoe",
  "is_active": true,
  "created_at": "2024-01-01T12:00:00"
}
```

## 2. User Login

Login to get an access token.

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=secretpass123"
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Save this token for authenticated requests!**

## 3. Get Current User

Get information about the currently authenticated user.

```bash
curl -X GET "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 4. Create a Product

Create a new product (requires authentication).

```bash
curl -X POST "http://localhost:8000/products/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "High-performance laptop for developers",
    "price": 1299.99,
    "stock": 15
  }'
```

**Response:**
```json
{
  "id": 1,
  "name": "Laptop",
  "description": "High-performance laptop for developers",
  "price": 1299.99,
  "stock": 15,
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-01T12:00:00"
}
```

## 5. List All Products

Get all products (cached for 5 minutes).

```bash
curl -X GET "http://localhost:8000/products/"
```

**Response:**
```json
[
  {
    "id": 1,
    "name": "Laptop",
    "description": "High-performance laptop for developers",
    "price": 1299.99,
    "stock": 15,
    "created_at": "2024-01-01T12:00:00",
    "updated_at": "2024-01-01T12:00:00"
  }
]
```

## 6. Get a Specific Product

Get details of a specific product by ID (cached).

```bash
curl -X GET "http://localhost:8000/products/1"
```

## 7. Update a Product

Update an existing product (requires authentication).

```bash
curl -X PUT "http://localhost:8000/products/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "price": 1199.99,
    "stock": 20
  }'
```

## 8. Create an Order

Create a new order (requires authentication).

```bash
curl -X POST "http://localhost:8000/orders/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "product_id": 1,
        "quantity": 2
      }
    ]
  }'
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "total_amount": 2599.98,
  "status": "pending",
  "created_at": "2024-01-01T12:00:00",
  "updated_at": "2024-01-01T12:00:00",
  "order_items": [
    {
      "id": 1,
      "product_id": 1,
      "quantity": 2,
      "price": 1299.99
    }
  ]
}
```

## 9. List User Orders

Get all orders for the authenticated user.

```bash
curl -X GET "http://localhost:8000/orders/" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 10. Get Order Details

Get details of a specific order.

```bash
curl -X GET "http://localhost:8000/orders/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 11. Complete an Order

Mark an order as completed.

```bash
curl -X PATCH "http://localhost:8000/orders/1/complete" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 12. Cancel an Order

Cancel a pending order (restores product stock).

```bash
curl -X PATCH "http://localhost:8000/orders/1/cancel" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 13. Delete a Product

Delete a product (requires authentication).

```bash
curl -X DELETE "http://localhost:8000/products/1" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Using Python Requests

Here's an example using Python:

```python
import requests

BASE_URL = "http://localhost:8000"

# Register
response = requests.post(f"{BASE_URL}/auth/register", json={
    "email": "user@example.com",
    "username": "testuser",
    "password": "password123"
})
print(response.json())

# Login
response = requests.post(f"{BASE_URL}/auth/login", data={
    "username": "testuser",
    "password": "password123"
})
token = response.json()["access_token"]

# Create product
headers = {"Authorization": f"Bearer {token}"}
response = requests.post(f"{BASE_URL}/products/", 
    headers=headers,
    json={
        "name": "Smartphone",
        "description": "Latest model",
        "price": 799.99,
        "stock": 50
    }
)
product = response.json()
print(product)

# Create order
response = requests.post(f"{BASE_URL}/orders/",
    headers=headers,
    json={
        "items": [{"product_id": product["id"], "quantity": 1}]
    }
)
print(response.json())
```

## Testing with Swagger UI

The easiest way to test the API is through the interactive Swagger documentation:

1. Start the server
2. Navigate to http://localhost:8000/docs
3. Click "Authorize" and enter your access token
4. Try out any endpoint directly from the browser!

## Environment Setup

Make sure to configure your `.env` file:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/ecommerce
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Error Responses

The API returns standard HTTP status codes:

- `200 OK`: Successful GET, PUT, PATCH
- `201 Created`: Successful POST
- `204 No Content`: Successful DELETE
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Missing or invalid token
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
