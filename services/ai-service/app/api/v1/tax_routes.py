"""Tax Calculation API Routes - FY 2025-26 Compliant"""
from fastapi import APIRouter, HTTPException
from ...agents.tax_calculator.calculator_fy2025 import (
    calculate_new_regime_tax_fy2025,
    calculate_old_regime_tax_fy2025,
    TaxCalculationInput
)
from ...models.tax_models import TaxData

router = APIRouter(prefix="/tax", tags=["tax-calculation-fy2025"])

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "tax-calculation",
        "compliance": "FY 2025-26 Budget 2025 Compliant"
    }

@router.post("/calculate")
async def calculate_tax(tax_data: TaxData):
    """Calculate tax using FY 2025-26 rules"""
    try:
        calc_input = TaxCalculationInput(
            gross_income=tax_data.income,
            age=tax_data.age,
            regime=tax_data.regime,
            is_salaried=tax_data.is_salaried,
            deductions_80c=tax_data.deductions_80c,
            health_insurance_premium=tax_data.health_insurance_premium
        )
        
        if tax_data.regime.lower() == "new":
            result = calculate_new_regime_tax_fy2025(calc_input)
        else:
            result = calculate_old_regime_tax_fy2025(calc_input)
        
        return {
            **result,
            "message": "FY 2025-26 tax calculation complete",
            "budget_compliance": "Union Budget 2025 Updated"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tax calculation failed: {str(e)}")

@router.post("/compare-regimes")
async def compare_regimes(tax_data: TaxData):
    """Compare tax in both regimes"""
    try:
        # New regime calculation
        new_input = TaxCalculationInput(
            gross_income=tax_data.income,
            age=tax_data.age,
            regime="new",
            is_salaried=tax_data.is_salaried
        )
        new_result = calculate_new_regime_tax_fy2025(new_input)
        
        # Old regime calculation
        old_input = TaxCalculationInput(
            gross_income=tax_data.income,
            age=tax_data.age,
            regime="old",
            is_salaried=tax_data.is_salaried,
            deductions_80c=tax_data.deductions_80c,
            health_insurance_premium=tax_data.health_insurance_premium
        )
        old_result = calculate_old_regime_tax_fy2025(old_input)
        
        savings = old_result["final_tax"] - new_result["final_tax"]
        recommended = "new" if savings > 0 else "old"
        
        return {
            "new_regime": new_result,
            "old_regime": old_result,
            "tax_savings_with_new_regime": savings,
            "recommended_regime": recommended,
            "compliance": "FY 2025-26 Budget Updated"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {str(e)}")
