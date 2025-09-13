"""
Tax calculation logic for Indian tax system FY 2025-26
Pure business logic without dependencies
"""

def calculate_new_regime_tax(taxable_income: float) -> float:
    """Calculate tax based on new regime slabs for FY 2025-26"""
    tax = 0
    
    if taxable_income > 0:
        tax += min(taxable_income, 400000) * 0.05  # 3L-7L: 5%
    if taxable_income > 400000:
        tax += min(taxable_income - 400000, 300000) * 0.10  # 7L-10L: 10%
    if taxable_income > 700000:
        tax += min(taxable_income - 700000, 200000) * 0.15  # 10L-12L: 15%
    if taxable_income > 900000:
        tax += min(taxable_income - 900000, 300000) * 0.20  # 12L-15L: 20%
    if taxable_income > 1200000:
        tax += (taxable_income - 1200000) * 0.30  # Above 15L: 30%
    
    # Add 4% cess
    tax = tax * 1.04
    return round(tax, 2)

def calculate_old_regime_tax(taxable_income: float) -> float:
    """Calculate tax based on old regime slabs for FY 2025-26"""
    tax = 0
    
    if taxable_income > 0:
        tax += min(taxable_income, 250000) * 0.05  # 2.5L-5L: 5%
    if taxable_income > 250000:
        tax += min(taxable_income - 250000, 500000) * 0.20  # 5L-10L: 20%
    if taxable_income > 750000:
        tax += (taxable_income - 750000) * 0.30  # Above 10L: 30%
    
    # Add 4% cess
    tax = tax * 1.04
    return round(tax, 2)

def get_tax_breakdown(taxable_income: float, regime: str) -> dict:
    """Get detailed tax breakdown for transparency"""
    breakdown = {
        "regime": regime,
        "taxable_income": taxable_income,
        "slabs": [],
        "total_tax": 0
    }
    
    if regime == "new":
        slabs = [
            (0, 400000, 0.05, "₹0 - ₹4L"),
            (400000, 700000, 0.10, "₹4L - ₹7L"),
            (700000, 900000, 0.15, "₹7L - ₹9L"),
            (900000, 1200000, 0.20, "₹9L - ₹12L"),
            (1200000, float('inf'), 0.30, "Above ₹12L")
        ]
    else:
        slabs = [
            (0, 250000, 0.05, "₹0 - ₹2.5L"),
            (250000, 750000, 0.20, "₹2.5L - ₹7.5L"),
            (750000, float('inf'), 0.30, "Above ₹7.5L")
        ]
    
    remaining_income = taxable_income
    
    for min_amount, max_amount, rate, description in slabs:
        if remaining_income <= 0:
            break
            
        slab_income = min(remaining_income, max_amount - min_amount)
        if slab_income > 0:
            slab_tax = slab_income * rate
            breakdown["slabs"].append({
                "range": description,
                "rate": f"{rate*100}%",
                "taxable_amount": slab_income,
                "tax": slab_tax
            })
            breakdown["total_tax"] += slab_tax
            remaining_income -= slab_income
    
    # Add cess
    cess = breakdown["total_tax"] * 0.04
    breakdown["cess"] = cess
    breakdown["total_tax_with_cess"] = breakdown["total_tax"] + cess
    
    return breakdown

