"""
Tax Calculator Agent - LangChain powered intelligent tax calculation
"""
from langchain_aws import ChatBedrockConverse
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from typing import Dict, Any
import boto3

from .calculator import (
    calculate_new_regime_tax, 
    calculate_old_regime_tax, 
    get_tax_breakdown
)
from ...models.tax_models import TaxData, TaxCalculationResult

class TaxCalculatorAgent:
    """
    Specialized agent for tax calculations with AI insights
    Combines precise mathematical calculations with intelligent recommendations
    """
    
    def __init__(self, aws_region: str = "us-east-1"):
        # Initialize AWS Bedrock client
        self.bedrock_client = boto3.client("bedrock-runtime", region_name=aws_region)
        
        # Use fast, cost-effective model for calculations
        self.llm = ChatBedrockConverse(
            client=self.bedrock_client,
            model="anthropic.claude-3-haiku-20240307-v1:0",
            model_kwargs={
                "temperature": 0.1,  # Low temperature for consistent calculations
                "max_tokens": 2000
            }
        )
        
        # Create structured prompt template
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are an expert Indian tax consultant for FY 2025-26. 
             Provide accurate, actionable tax advice based on current Indian tax laws.
             Be specific with amounts and deadlines."""),
            ("human", """
            Tax calculation completed for:
            - Annual Income: ₹{income:,.0f}
            - Age: {age}
            - Tax Regime: {regime}
            - Calculated Tax: ₹{calculated_tax:,.0f}
            - Taxable Income: ₹{taxable_income:,.0f}
            
            Tax Breakdown: {breakdown}
            
            Provide:
            1. Verification of calculation accuracy
            2. 3 specific tax-saving recommendations with exact amounts
            3. Upcoming deadlines and compliance requirements
            4. Comparison with alternative regime if beneficial
            
            Keep recommendations practical and implementable.
            """)
        ])
        
        # Create processing chain
        self.processing_chain = (
            self.prompt_template 
            | self.llm 
            | StrOutputParser()
        )
    
    async def calculate_tax(self, tax_data: TaxData) -> TaxCalculationResult:
        """
        Main method: Calculate tax with AI insights
        
        Args:
            tax_data: User's tax information
            
        Returns:
            TaxCalculationResult with calculation and AI insights
        """
        try:
            # Determine exemption based on regime
            exemption = 300000 if tax_data.regime.lower() == "new" else 250000
            taxable_income = max(0, tax_data.income - exemption)
            
            # Calculate tax using appropriate regime
            if tax_data.regime.lower() == "new":
                calculated_tax = calculate_new_regime_tax(taxable_income)
            else:
                calculated_tax = calculate_old_regime_tax(taxable_income)
            
            # Get detailed breakdown
            breakdown = get_tax_breakdown(taxable_income, tax_data.regime.lower())
            
            # Generate AI insights
            ai_insights = await self.processing_chain.ainvoke({
                "income": tax_data.income,
                "age": tax_data.age,
                "regime": tax_data.regime,
                "calculated_tax": calculated_tax,
                "taxable_income": taxable_income,
                "breakdown": breakdown
            })
            
            # Calculate effective tax rate
            effective_rate = (calculated_tax / tax_data.income * 100) if tax_data.income > 0 else 0
            
            return TaxCalculationResult(
                gross_income=tax_data.income,
                taxable_income=taxable_income,
                exemption=exemption,
                tax_amount=calculated_tax,
                effective_tax_rate=round(effective_rate, 2),
                regime=tax_data.regime,
                breakdown=breakdown,
                ai_insights=ai_insights,
                agent_used="TaxCalculatorAgent"
            )
            
        except Exception as e:
            # Fallback calculation without AI
            exemption = 300000 if tax_data.regime.lower() == "new" else 250000
            taxable_income = max(0, tax_data.income - exemption)
            
            if tax_data.regime.lower() == "new":
                calculated_tax = calculate_new_regime_tax(taxable_income)
            else:
                calculated_tax = calculate_old_regime_tax(taxable_income)
            
            return TaxCalculationResult(
                gross_income=tax_data.income,
                taxable_income=taxable_income,
                exemption=exemption,
                tax_amount=calculated_tax,
                effective_tax_rate=round((calculated_tax / tax_data.income * 100), 2),
                regime=tax_data.regime,
                ai_insights=f"Calculation completed successfully. AI insights unavailable due to: {str(e)}",
                agent_used="TaxCalculatorAgent (Fallback Mode)",
                error=str(e)
            )
    
    async def compare_regimes(self, tax_data: TaxData) -> Dict[str, Any]:
        """Compare tax liability in both regimes"""
        new_regime_data = TaxData(income=tax_data.income, age=tax_data.age, regime="new")
        old_regime_data = TaxData(income=tax_data.income, age=tax_data.age, regime="old")
        
        new_result = await self.calculate_tax(new_regime_data)
        old_result = await self.calculate_tax(old_regime_data)
        
        savings = old_result.tax_amount - new_result.tax_amount
        recommended_regime = "new" if savings > 0 else "old"
        
        return {
            "new_regime": new_result.dict(),
            "old_regime": old_result.dict(),
            "savings_with_new_regime": savings,
            "recommended_regime": recommended_regime,
            "recommendation_reason": f"Save ₹{abs(savings):,.0f} with {recommended_regime} regime"
        }

