"""
Unit tests for tax calculation functions
"""
import pytest
from app.agents.tax_calculator.calculator import (
    calculate_new_regime_tax,
    calculate_old_regime_tax,
    get_tax_breakdown
)

def test_new_regime_calculation():
    """Test new regime tax calculation"""
    # Test case: ₹10 lakh income
    taxable_income = 700000  # 10L - 3L exemption
    expected_tax = 52000.0   # Your known result
    
    calculated_tax = calculate_new_regime_tax(taxable_income)
    assert calculated_tax == expected_tax

def test_old_regime_calculation():
    """Test old regime tax calculation"""
    taxable_income = 750000  # 10L - 2.5L exemption
    calculated_tax = calculate_old_regime_tax(taxable_income)
    
    # Should be higher than new regime
    assert calculated_tax > 52000

def test_tax_breakdown():
    """Test detailed tax breakdown"""
    breakdown = get_tax_breakdown(700000, "new")
    
    assert breakdown["regime"] == "new"
    assert breakdown["taxable_income"] == 700000
    assert len(breakdown["slabs"]) == 2  # Two slabs applied
    assert breakdown["total_tax_with_cess"] > breakdown["total_tax"]

