# E-Commerce Backend API

A complete e-commerce backend built with FastAPI, PostgreSQL, and Redis featuring authentication, order management, caching, and comprehensive Swagger documentation.

## Features

- **FastAPI Framework**: Modern, fast, and async Python web framework
- **PostgreSQL Database**: Relational database for data persistence
- **Redis Caching**: Fast in-memory caching for product listings
- **JWT Authentication**: Secure token-based authentication
- **Order Management**: Complete order lifecycle management
- **Swagger Documentation**: Interactive API documentation at `/docs`
- **Docker Support**: Easy deployment with Docker Compose

## Tech Stack

- **FastAPI**: Web framework
- **SQLAlchemy**: ORM for database operations
- **PostgreSQL**: Primary database
- **Redis**: Caching layer
- **Pydantic**: Data validation
- **python-jose**: JWT token handling
- **passlib**: Password hashing

## Project Structure

```
e-commerce-project/
├── app/
│   ├── core/
│   │   ├── config.py      # Configuration settings
│   │   ├── database.py    # Database connection
│   │   ├── cache.py       # Redis connection
│   │   └── security.py    # Authentication utilities
│   ├── models/
│   │   └── models.py      # SQLAlchemy models
│   ├── schemas/
│   │   └── schemas.py     # Pydantic schemas
│   ├── routes/
│   │   ├── auth.py        # Authentication endpoints
│   │   ├── products.py    # Product endpoints
│   │   └── orders.py      # Order endpoints
│   └── main.py            # FastAPI application
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11+
- Docker and Docker Compose (recommended)
- PostgreSQL 15+ (if running locally)
- Redis 7+ (if running locally)

### Installation

#### Option 1: Using Docker Compose (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/yvonnegichovi/e-commerce-project.git
cd e-commerce-project
```

2. Start the services:
```bash
docker-compose up -d
```

3. Access the API:
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### Option 2: Local Installation

1. Clone the repository:
```bash
git clone https://github.com/yvonnegichovi/e-commerce-project.git
cd e-commerce-project
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your database and Redis URLs
```

5. Start PostgreSQL and Redis:
```bash
# Make sure PostgreSQL and Redis are running
```

6. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

### Authentication

- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get access token
- `GET /auth/me` - Get current user information

### Products

- `GET /products` - List all products (cached)
- `GET /products/{id}` - Get a specific product (cached)
- `POST /products` - Create a new product (requires auth)
- `PUT /products/{id}` - Update a product (requires auth)
- `DELETE /products/{id}` - Delete a product (requires auth)

### Orders

- `POST /orders` - Create a new order (requires auth)
- `GET /orders` - List user's orders (requires auth)
- `GET /orders/{id}` - Get a specific order (requires auth)
- `PATCH /orders/{id}/cancel` - Cancel an order (requires auth)
- `PATCH /orders/{id}/complete` - Complete an order (requires auth)

## API Documentation

Once the application is running, visit:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

The Swagger UI provides interactive documentation where you can test all endpoints directly from your browser.

## Authentication

This API uses JWT (JSON Web Tokens) for authentication:

1. Register a new user at `/auth/register`
2. Login at `/auth/login` to receive an access token
3. Include the token in the Authorization header for protected endpoints:
   ```
   Authorization: Bearer <your-access-token>
   ```

## Caching

Redis is used to cache:
- Product listings (`/products`)
- Individual products (`/products/{id}`)

Cache is automatically invalidated when products are created, updated, or deleted.

## Database Models

### User
- id, email, username, hashed_password, is_active, created_at

### Product
- id, name, description, price, stock, created_at, updated_at

### Order
- id, user_id, total_amount, status, created_at, updated_at

### OrderItem
- id, order_id, product_id, quantity, price

## Environment Variables

```env
DATABASE_URL=postgresql://user:password@localhost:5432/ecommerce
REDIS_URL=redis://localhost:6379
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

### Code Formatting

```bash
# Install dev dependencies
pip install black isort

# Format code
black .
isort .
```

## Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild services
docker-compose up -d --build
```

## Example Usage

### Register a User

```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "johndoe",
    "password": "secretpassword"
  }'
```

### Login

```bash
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=secretpassword"
```

### Create a Product

```bash
curl -X POST "http://localhost:8000/products" \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "High-performance laptop",
    "price": 999.99,
    "stock": 10
  }'
```

### Create an Order

```bash
curl -X POST "http://localhost:8000/orders" \
  -H "Authorization: Bearer <your-token>" \
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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.