"""Enhanced Tax Models for FY 2025-26"""
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime

class TaxData(BaseModel):
    income: float = Field(..., description="Gross annual income", gt=0)
    age: int = Field(..., description="Age of taxpayer", ge=18, le=100)
    regime: str = Field(..., description="Tax regime: 'new' or 'old'")
    is_salaried: bool = Field(True, description="Is taxpayer salaried")
    deductions_80c: float = Field(0, description="Section 80C deductions", ge=0, le=150000)
    health_insurance_premium: float = Field(0, description="Health insurance premium", ge=0)
    
    @validator('regime')
    def validate_regime(cls, v):
        if v.lower() not in ['new', 'old']:
            raise ValueError('Regime must be "new" or "old"')
        return v.lower()

class TaxCalculationResult(BaseModel):
    gross_income: float
    final_tax: float
    regime: str
    financial_year: str
    compliance_status: str
    breakdown: List[Dict[str, Any]]
    timestamp: datetime = Field(default_factory=datetime.now)
