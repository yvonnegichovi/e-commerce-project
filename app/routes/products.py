from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import json
from app.core.database import get_db
from app.core.cache import redis_client
from app.models.models import User, Product
from app.schemas.schemas import ProductCreate, ProductUpdate, ProductResponse
from app.routes.auth import get_current_user

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    # Invalidate cache
    redis_client.delete("products:all")
    
    return db_product


@router.get("/", response_model=List[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    # Try to get from cache
    cached_products = redis_client.get("products:all")
    if cached_products:
        products_data = json.loads(cached_products)
        return [ProductResponse(**p) for p in products_data]
    
    # Get from database
    products = db.query(Product).all()
    
    # Cache the results
    products_data = [ProductResponse.model_validate(p).model_dump(mode='json') for p in products]
    redis_client.setex("products:all", 300, json.dumps(products_data, default=str))
    
    return products


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    # Try to get from cache
    cache_key = f"product:{product_id}"
    cached_product = redis_client.get(cache_key)
    if cached_product:
        return ProductResponse(**json.loads(cached_product))
    
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    # Cache the result
    product_data = ProductResponse.model_validate(product).model_dump(mode='json')
    redis_client.setex(cache_key, 300, json.dumps(product_data, default=str))
    
    return product


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    update_data = product_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(product, field, value)
    
    db.commit()
    db.refresh(product)
    
    # Invalidate cache
    redis_client.delete(f"product:{product_id}")
    redis_client.delete("products:all")
    
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    db.delete(product)
    db.commit()
    
    # Invalidate cache
    redis_client.delete(f"product:{product_id}")
    redis_client.delete("products:all")
    
    return None
