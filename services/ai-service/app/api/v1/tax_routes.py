"""
FastAPI routes for tax calculation endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any

from ...agents.tax_calculator.agent import TaxCalculatorAgent
from ...models.tax_models import TaxData, TaxCalculationResult, ComparisonResult
from ...core.dependencies import get_tax_calculator_agent

router = APIRouter(prefix="/tax", tags=["tax-calculation"])

@router.get("/health")
async def health_check():
    """Health check for tax calculation service"""
    return {
        "status": "healthy", 
        "service": "tax-calculator-agent",
        "agent": "TaxCalculatorAgent"
    }

@router.post("/calculate", response_model=TaxCalculationResult)
async def calculate_tax(
    tax_data: TaxData,
    agent: TaxCalculatorAgent = Depends(get_tax_calculator_agent)
) -> TaxCalculationResult:
    """Calculate tax with AI insights"""
    try:
        result = await agent.calculate_tax(tax_data)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tax calculation failed: {str(e)}")

@router.post("/compare-regimes")
async def compare_regimes(
    tax_data: TaxData,
    agent: TaxCalculatorAgent = Depends(get_tax_calculator_agent)
) -> Dict[str, Any]:
    """Compare tax liability in both regimes"""
    try:
        # Remove regime specification for comparison
        comparison_data = TaxData(income=tax_data.income, age=tax_data.age, regime="new")
        result = await agent.compare_regimes(comparison_data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Regime comparison failed: {str(e)}")

@router.get("/tax-slabs/{regime}")
async def get_tax_slabs(regime: str):
    """Get current tax slabs for specified regime"""
    if regime.lower() not in ['new', 'old']:
        raise HTTPException(status_code=400, detail="Regime must be 'new' or 'old'")
    
    if regime.lower() == "new":
        slabs = [
            {"range": "₹0 - ₹3,00,000", "rate": "0%"},
            {"range": "₹3,00,001 - ₹7,00,000", "rate": "5%"},
            {"range": "₹7,00,001 - ₹10,00,000", "rate": "10%"},
            {"range": "₹10,00,001 - ₹12,00,000", "rate": "15%"},
            {"range": "₹12,00,001 - ₹15,00,000", "rate": "20%"},
            {"range": "Above ₹15,00,000", "rate": "30%"}
        ]
    else:
        slabs = [
            {"range": "₹0 - ₹2,50,000", "rate": "0%"},
            {"range": "₹2,50,001 - ₹5,00,000", "rate": "5%"},
            {"range": "₹5,00,001 - ₹10,00,000", "rate": "20%"},
            {"range": "Above ₹10,00,000", "rate": "30%"}
        ]
    
    return {
        "regime": regime.lower(),
        "financial_year": "2025-26",
        "slabs": slabs,
        "cess": "4% on total tax",
        "standard_deduction": "₹50,000" if regime.lower() == "new" else "Not applicable"
    }

