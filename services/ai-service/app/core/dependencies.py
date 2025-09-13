"""
FastAPI dependency injection
"""
from functools import lru_cache
from ..agents.tax_calculator.agent import TaxCalculatorAgent

@lru_cache()
def get_tax_calculator_agent() -> TaxCalculatorAgent:
    """Dependency injection for Tax Calculator Agent"""
    return TaxCalculatorAgent(aws_region="us-east-1")

