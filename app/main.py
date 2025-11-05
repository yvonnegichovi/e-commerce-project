from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, products, orders

app = FastAPI(
    title="E-Commerce API",
    description="A FastAPI-based e-commerce backend with PostgreSQL and Redis",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(products.router)
app.include_router(orders.router)


@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    from app.core.database import engine, Base
    Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Welcome to E-Commerce API",
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}
