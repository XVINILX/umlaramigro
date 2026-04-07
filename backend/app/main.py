from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core import engine, Base
from app.core.config import settings
from app.core.mongodb import close_mongo_connection
from app.routes import (
    auth_router,
    organizations_router,
    pets_router,
    interest_forms_router,
)
from app.repositories.factory import RepositoryFactory

# Create tables
Base.metadata.create_all(bind=engine)

# Configure repository backend
RepositoryFactory.set_backend(settings.REPOSITORY_BACKEND)

app = FastAPI(
    title="UmlAramigo API",
    description="API para plataforma de doação de pets",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Event handlers
@app.on_event("startup")
async def startup():
    """Executado ao iniciar a aplicação."""
    print(f"✓ Backend de repositório configurado para: {settings.REPOSITORY_BACKEND}")


@app.on_event("shutdown")
async def shutdown():
    """Executado ao desligar a aplicação."""
    if settings.REPOSITORY_BACKEND == "mongodb":
        await close_mongo_connection()

# Include routers
app.include_router(auth_router)
app.include_router(organizations_router)
app.include_router(pets_router)
app.include_router(interest_forms_router)

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to UmlAramigo API",
        "docs": "/docs",
        "redoc": "/redoc",
    }

@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}
