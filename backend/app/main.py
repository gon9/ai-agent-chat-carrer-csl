from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.config import settings

def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application
    """
    application = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.VERSION,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc",
    )
    
    # Include API router
    application.include_router(api_router, prefix=settings.API_V1_STR)
    
    return application

app = create_application()

@app.get("/")
async def root():
    """
    Root endpoint that redirects to the API documentation
    """
    return {"message": "Welcome to the API. Visit /api/v1/docs for documentation"}
