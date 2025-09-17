"""Main FastAPI Application - FY 2025-26 Compliant"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.tax_routes import router as tax_router
from .api.v1.auth_routes import router as auth_router

def create_application() -> FastAPI:
    app = FastAPI(
        title="AI Tax Compliance Platform - FY 2025-26",
        description="Updated for Union Budget 2025 - Zero tax up to ₹12 lakh!",
        version="2.1.0"
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE"],
        allow_headers=["*"],
    )
    
    app.include_router(tax_router, prefix="/api/v1")
    app.include_router(auth_router, prefix="/api/v1")
    
    return app

app = create_application()

@app.get("/")
async def root():
    return {
        "message": "AI Tax Compliance Platform - FY 2025-26",
        "compliance": "Union Budget 2025 Updated",
        "key_updates": [
            "Zero tax up to ₹12 lakh income",
            "Basic exemption increased to ₹4 lakh",
            "Section 87A rebate increased to ₹60,000",
            "New 25% tax slab for ₹20L-₹24L",
            "Standard deduction increased to ₹75,000"
        ],
        "status": "active"
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "tax-ai-service-fy2025"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
