from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.routers import auth, agents, ratings_reviews

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Agent Marketplace API",
    description="A marketplace for AI agents where users can create, share, and deploy agents",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(agents.router, prefix="/agents", tags=["Agents"])
app.include_router(ratings_reviews.router, prefix="/api", tags=["Ratings & Reviews"])


@app.get("/")
async def root():
    return {
        "message": "Welcome to Agent Marketplace API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
