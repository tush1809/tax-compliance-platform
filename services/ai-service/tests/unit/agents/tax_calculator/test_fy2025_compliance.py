"""Unit tests for FY 2025-26 tax calculator"""
import pytest
import sys
import os

# Add the app directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../../../'))

from app.agents.tax_calculator.calculator_fy2025 import (
    calculate_new_regime_tax_fy2025,
    calculate_old_regime_tax_fy2025,
    TaxCalculationInput
)

def test_zero_tax_up_to_12_lakh():
    """Test zero tax up to ₹12 lakh due to ₹60,000 rebate"""
    calc_input = TaxCalculationInput(
        gross_income=1200000,
        age=30,
        regime="new",
        is_salaried=True
    )
    
    result = calculate_new_regime_tax_fy2025(calc_input)
    
    assert result["final_tax"] == 0.0
    assert result["rebate_87a"] == 60000
    assert result["basic_exemption"] == 400000

def test_new_exemption_4_lakh():
    """Test new ₹4 lakh exemption"""
    calc_input = TaxCalculationInput(
        gross_income=475000,
        age=25,
        regime="new"
    )
    
    result = calculate_new_regime_tax_fy2025(calc_input)
    
    assert result["basic_exemption"] == 400000
    assert result["final_tax"] == 0.0

def test_age_based_exemptions():
    """Test age-based exemptions in old regime"""
    calc_input = TaxCalculationInput(
        gross_income=500000,
        age=85,
        regime="old"
    )
    
    result = calculate_old_regime_tax_fy2025(calc_input)
    
    assert result["basic_exemption"] == 500000
    assert result["final_tax"] == 0.0

def test_new_25_percent_slab():
    """Test new 25% slab for ₹20L-₹24L"""
    calc_input = TaxCalculationInput(
        gross_income=2200000,
        age=35,
        regime="new"
    )
    
    result = calculate_new_regime_tax_fy2025(calc_input)
    
    # Should have 25% slab in breakdown
    has_25_percent = any(
        slab["rate"] == "25%" for slab in result["breakdown"]
    )
    assert has_25_percent, "25% slab not found"
