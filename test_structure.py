#!/usr/bin/env python3
"""
Validate the FastAPI e-commerce application structure and endpoints.
"""

from app.main import app


def test_app_metadata():
    """Test application metadata"""
    assert app.title == "E-Commerce API"
    assert app.version == "1.0.0"
    print("✓ App metadata is correct")


def test_routes():
    """Test that all required routes are registered"""
    routes = [route.path for route in app.routes]
    
    required_routes = [
        "/",
        "/health",
        "/auth/register",
        "/auth/login",
        "/auth/me",
        "/products/",
        "/products/{product_id}",
        "/orders/",
        "/orders/{order_id}",
        "/orders/{order_id}/cancel",
        "/orders/{order_id}/complete",
    ]
    
    for required_route in required_routes:
        assert required_route in routes, f"Missing route: {required_route}"
    
    print(f"✓ All {len(required_routes)} required routes are registered")


def test_openapi_docs():
    """Test OpenAPI documentation"""
    openapi_schema = app.openapi()
    
    assert "openapi" in openapi_schema
    assert "info" in openapi_schema
    assert "paths" in openapi_schema
    
    # Check authentication endpoints
    assert "/auth/register" in openapi_schema["paths"]
    assert "/auth/login" in openapi_schema["paths"]
    
    # Check product endpoints
    assert "/products/" in openapi_schema["paths"]
    assert "/products/{product_id}" in openapi_schema["paths"]
    
    # Check order endpoints
    assert "/orders/" in openapi_schema["paths"]
    assert "/orders/{order_id}" in openapi_schema["paths"]
    
    print("✓ OpenAPI documentation is properly configured")


def test_components():
    """Test that all components are importable"""
    from app.core import config, database, cache, security
    from app.models import models
    from app.schemas import schemas
    from app.routes import auth, products, orders
    
    print("✓ All components are importable")


if __name__ == "__main__":
    print("Testing E-Commerce API structure...\n")
    
    test_app_metadata()
    test_routes()
    test_openapi_docs()
    test_components()
    
    print("\n✅ All tests passed!")
