"""
Main FastAPI application - Clean and focused
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.tax_routes import router as tax_router
from .core.config import settings

def create_application() -> FastAPI:
    """Application factory"""
    
    app = FastAPI(
        title="Tax AI Service - Multi-Agent Architecture",
        description="Intelligent tax calculation with specialized AI agents",
        version="2.0.0"
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(tax_router, prefix="/api/v1")
    
    return app

app = create_application()

@app.get("/")
async def root():
    return {
        "message": "Tax AI Service - Multi-Agent Architecture",
        "agents": ["TaxCalculatorAgent"],
        "status": "active"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "tax-ai-service"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

