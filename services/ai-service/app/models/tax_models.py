"""
Pydantic models for tax-related data structures
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class TaxData(BaseModel):
    """Input data for tax calculations"""
    income: float = Field(..., description="Annual gross income", gt=0)
    age: int = Field(..., description="Age of taxpayer", ge=18, le=100)
    regime: str = Field(..., description="Tax regime: 'new' or 'old'")
    
    @validator('regime')
    def validate_regime(cls, v):
        if v.lower() not in ['new', 'old']:
            raise ValueError('Regime must be "new" or "old"')
        return v.lower()

class TaxSlabInfo(BaseModel):
    """Information about a tax slab"""
    range: str
    rate: str
    taxable_amount: float
    tax: float

class TaxBreakdown(BaseModel):
    """Detailed tax calculation breakdown"""
    regime: str
    taxable_income: float
    slabs: List[TaxSlabInfo]
    total_tax: float
    cess: float
    total_tax_with_cess: float

class TaxCalculationResult(BaseModel):
    """Complete tax calculation result"""
    gross_income: float
    taxable_income: float
    exemption: float
    tax_amount: float
    effective_tax_rate: float
    regime: str
    breakdown: Dict[str, Any]
    ai_insights: str
    agent_used: str
    timestamp: datetime = Field(default_factory=datetime.now)
    error: Optional[str] = None

class ComparisonResult(BaseModel):
    """Result of regime comparison"""
    new_regime: TaxCalculationResult
    old_regime: TaxCalculationResult
    savings_with_new_regime: float
    recommended_regime: str
    recommendation_reason: str

