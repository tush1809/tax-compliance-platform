"""
FY 2025-26 Tax Calculator - Union Budget 2025 Compliant
Based on official tax law changes from your provided document
"""
from typing import Dict, Any
from dataclasses import dataclass

@dataclass
class TaxCalculationInput:
    gross_income: float
    age: int
    regime: str
    is_salaried: bool = True
    deductions_80c: float = 0
    health_insurance_premium: float = 0

def calculate_new_regime_tax_fy2025(calc_input: TaxCalculationInput) -> Dict[str, Any]:
    """Calculate tax using FY 2025-26 new regime - Budget 2025 compliant"""
    
    # Standard deduction increased to ₹75,000
    standard_deduction = 75000 if calc_input.is_salaried else 0
    income_after_std_deduction = max(0, calc_input.gross_income - standard_deduction)
    
    # Basic exemption increased from ₹3L to ₹4L
    basic_exemption = 400000
    taxable_income = max(0, income_after_std_deduction - basic_exemption)
    
    # FY 2025-26 tax slabs (from your official document)
    tax = 0
    breakdown = []
    
    slabs = [
        (400000, 0.05, "₹4L - ₹8L"),     # ₹4L-₹8L: 5%
        (400000, 0.10, "₹8L - ₹12L"),   # ₹8L-₹12L: 10%
        (400000, 0.15, "₹12L - ₹16L"),  # ₹12L-₹16L: 15%
        (400000, 0.20, "₹16L - ₹20L"),  # ₹16L-₹20L: 20%
        (400000, 0.25, "₹20L - ₹24L"),  # ₹20L-₹24L: 25% (NEW!)
        (float('inf'), 0.30, "Above ₹24L") # Above ₹24L: 30%
    ]
    
    remaining_income = taxable_income
    
    for slab_width, rate, description in slabs:
        if remaining_income <= 0:
            break
        
        slab_taxable = min(remaining_income, slab_width)
        if slab_taxable > 0:
            slab_tax = slab_taxable * rate
            tax += slab_tax
            
            breakdown.append({
                "slab": description,
                "rate": f"{rate*100}%",
                "taxable_amount": slab_taxable,
                "tax": slab_tax
            })
            
            remaining_income -= slab_taxable
    
    # Add 4% cess
    tax_with_cess = tax * 1.04
    
    # Section 87A rebate increased to ₹60,000 (up to ₹12L income)
    rebate_87a = 0
    if income_after_std_deduction <= 1200000:
        rebate_87a = min(tax_with_cess, 60000)  # Max ₹60,000 rebate
    
    final_tax = max(0, tax_with_cess - rebate_87a)
    
    return {
        "gross_income": calc_input.gross_income,
        "standard_deduction": standard_deduction,
        "basic_exemption": basic_exemption,
        "taxable_income": taxable_income,
        "tax_before_cess": tax,
        "cess": tax * 0.04,
        "tax_after_cess": tax_with_cess,
        "rebate_87a": rebate_87a,
        "final_tax": final_tax,
        "effective_rate": (final_tax / calc_input.gross_income * 100) if calc_input.gross_income > 0 else 0,
        "breakdown": breakdown,
        "regime": "new",
        "financial_year": "2025-26",
        "compliance_status": "Budget 2025 Compliant"
    }

def calculate_old_regime_tax_fy2025(calc_input: TaxCalculationInput) -> Dict[str, Any]:
    """Calculate tax using old regime with age-based exemptions"""
    
    # Age-based exemption limits
    if calc_input.age >= 80:
        basic_exemption = 500000  # Super senior citizens
    elif calc_input.age >= 60:
        basic_exemption = 300000  # Senior citizens
    else:
        basic_exemption = 250000  # Below 60 years
    
    # Calculate deductions
    total_deductions = calc_input.deductions_80c + calc_input.health_insurance_premium
    
    # Calculate taxable income
    income_after_deductions = max(0, calc_input.gross_income - total_deductions)
    taxable_income = max(0, income_after_deductions - basic_exemption)
    
    # Old regime slabs
    tax = 0
    breakdown = []
    
    if taxable_income > 0:
        # ₹0 - ₹2.5L: 5%
        slab1 = min(taxable_income, 250000)
        if slab1 > 0:
            tax1 = slab1 * 0.05
            tax += tax1
            breakdown.append({
                "slab": "₹2.5L - ₹5L",
                "rate": "5%",
                "taxable_amount": slab1,
                "tax": tax1
            })
    
    if taxable_income > 250000:
        # ₹2.5L - ₹10L: 20%
        slab2 = min(taxable_income - 250000, 750000)
        tax2 = slab2 * 0.20
        tax += tax2
        breakdown.append({
            "slab": "₹5L - ₹10L", 
            "rate": "20%",
            "taxable_amount": slab2,
            "tax": tax2
        })
    
    if taxable_income > 1000000:
        # Above ₹10L: 30%
        slab3 = taxable_income - 1000000
        tax3 = slab3 * 0.30
        tax += tax3
        breakdown.append({
            "slab": "Above ₹10L",
            "rate": "30%",
            "taxable_amount": slab3,
            "tax": tax3
        })
    
    # Add 4% cess
    tax_with_cess = tax * 1.04
    
    # Section 87A rebate (old regime)
    rebate_87a = 0
    if income_after_deductions <= 500000:
        rebate_87a = min(tax_with_cess, 12500)  # Max ₹12,500
    
    final_tax = max(0, tax_with_cess - rebate_87a)
    
    return {
        "gross_income": calc_input.gross_income,
        "total_deductions": total_deductions,
        "basic_exemption": basic_exemption,
        "taxable_income": taxable_income,
        "tax_before_cess": tax,
        "cess": tax * 0.04,
        "tax_after_cess": tax_with_cess,
        "rebate_87a": rebate_87a,
        "final_tax": final_tax,
        "effective_rate": (final_tax / calc_input.gross_income * 100) if calc_input.gross_income > 0 else 0,
        "breakdown": breakdown,
        "regime": "old",
        "financial_year": "2025-26",
        "age_category": "super_senior" if calc_input.age >= 80 else "senior" if calc_input.age >= 60 else "regular"
    }
