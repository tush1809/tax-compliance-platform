"""
Tax Calculation API Routes - WITH AI INSIGHTS INTEGRATION
"""
from fastapi import APIRouter, HTTPException
import time
import logging

from ...agents.tax_calculator.calculator_fy2025 import (
    calculate_new_regime_tax_fy2025,
    calculate_old_regime_tax_fy2025,
    TaxCalculationInput
)
from ...models.tax_models import TaxData
from ...services.ai_service import ai_service

router = APIRouter(prefix="/tax", tags=["ai-powered-tax-calculation"])
logger = logging.getLogger(__name__)

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "ai-powered-tax-calculation",
        "ai_enabled": ai_service.is_available(),
        "compliance": "FY 2025-26 Budget 2025 Compliant",
        "model": "Claude 3 Haiku" if ai_service.is_available() else "None"
    }

@router.post("/calculate")
async def calculate_tax_with_ai_insights(tax_data: TaxData):
    """
    Calculate tax using FY 2025-26 rules WITH AI-POWERED INSIGHTS
    """
    start_time = time.time()
    
    try:
        # Step 1: Perform deterministic tax calculation
        calc_input = TaxCalculationInput(
            gross_income=tax_data.income,
            age=tax_data.age,
            regime=tax_data.regime,
            is_salaried=tax_data.is_salaried,
            deductions_80c=tax_data.deductions_80c,
            health_insurance_premium=tax_data.health_insurance_premium
        )
        
        if tax_data.regime.lower() == "new":
            calculation_result = calculate_new_regime_tax_fy2025(calc_input)
        else:
            calculation_result = calculate_old_regime_tax_fy2025(calc_input)
        
        # Step 2: Generate AI insights
        logger.info("Generating AI insights...")
        try:
            ai_insights = await ai_service.generate_tax_insights(
                tax_data=tax_data.dict(),
                calculation_result=calculation_result
            )
        except Exception as e:
            logger.error(f"AI insights generation failed: {e}")
            ai_insights = "AI insights temporarily unavailable due to technical issues"
        
        # Step 3: Calculate processing time
        processing_time = (time.time() - start_time) * 1000
        
        # Step 4: Return enhanced response with AI insights
        return {
            **calculation_result,
            "ai_insights": ai_insights,
            "ai_powered": True,
            "processing_time_ms": round(processing_time, 2),
            "ai_service_status": "active" if ai_service.is_available() else "disabled",
            "message": "AI-powered FY 2025-26 tax calculation completed",
            "budget_compliance": "Union Budget 2025 Updated with AI Analysis"
        }
        
    except Exception as e:
        logger.error(f"Tax calculation failed: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"AI-powered tax calculation failed: {str(e)}"
        )

@router.get("/ai-status")
async def get_ai_service_status():
    """Get current AI service status and configuration"""
    return {
        "ai_service_available": ai_service.is_available(),
        "model_id": ai_service.model_id if ai_service.is_available() else None,
        "aws_region": ai_service.region,
        "client_initialized": ai_service.client is not None,
        "features": {
            "tax_insights": ai_service.is_available(),
            "regime_comparison": ai_service.is_available(),
            "personalized_advice": ai_service.is_available()
        }
    }
