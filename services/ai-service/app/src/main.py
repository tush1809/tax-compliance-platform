from fastapi import FastAPI
from pydantic import BaseModel
import boto3
from langchain_aws import ChatBedrockConverse

app = FastAPI(title="Tax AI Service - Powered by AWS Bedrock")

# Initialize Bedrock client
bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")

# Initialize Bedrock LLM (Haiku works on-demand)
llm = ChatBedrockConverse(
    client=bedrock_client,
    model="anthropic.claude-3-haiku-20240307-v1:0"
)

class TaxData(BaseModel):
    income: float
    age: int
    regime: str

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "tax-ai-service"}

@app.post("/calculate-tax")
async def calculate_tax(tax_data: TaxData):
    """Basic tax calculation with AI insights"""
    
    # Create tax calculation prompt
    prompt = f"""
    Calculate Indian income tax for:
    - Annual Income: ₹{tax_data.income:,.2f}
    - Age: {tax_data.age}
    - Tax Regime: {tax_data.regime}
    
    Provide:
    1. Exact tax calculation
    2. Tax-saving recommendations
    3. Applicable deductions
    
    Focus on Indian tax laws for FY 2024-25.
    """
    
    try:
        # Get AI response
        response = await llm.ainvoke(prompt)
        
        # Basic tax calculation (manual fallback logic)
        if tax_data.regime == "new":
            taxable_income = max(0, tax_data.income - 300000)
            tax_amount = calculate_new_regime_tax(taxable_income)
        else:
            taxable_income = max(0, tax_data.income - 250000)
            tax_amount = calculate_old_regime_tax(taxable_income)
        
        return {
            "taxAmount": tax_amount,
            "taxableIncome": taxable_income,
            "aiInsights": response.content if hasattr(response, "content") else str(response),
            "regime": tax_data.regime
        }
    except Exception as e:
        return {"error": str(e)}

def calculate_new_regime_tax(taxable_income):
    """Calculate tax based on new regime slabs"""
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

def calculate_old_regime_tax(taxable_income):
    """Calculate tax based on old regime slabs"""
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


