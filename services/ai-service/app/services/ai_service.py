"""
AI Service - AWS Bedrock Integration with Retry Logic
"""
import boto3
import json
import asyncio
import logging
from typing import Dict, Any, Optional
from botocore.exceptions import ClientError, NoCredentialsError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BedrockAIService:
    """AWS Bedrock AI service with retry logic and error handling"""
    
    def __init__(self):
        self.client = None
        self.model_id = "anthropic.claude-3-haiku-20240307-v1:0"
        self.region = "us-east-1"
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize AWS Bedrock client with error handling"""
        try:
            self.client = boto3.client(
                'bedrock-runtime',
                region_name=self.region
            )
            logger.info("AWS Bedrock client initialized successfully")
        except NoCredentialsError:
            logger.error("AWS credentials not found. AI features will be disabled.")
            self.client = None
        except Exception as e:
            logger.error(f"Failed to initialize AWS Bedrock client: {e}")
            self.client = None
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(ClientError)
    )
    async def invoke_model_with_retry(self, prompt: str, max_tokens: int = 2000) -> str:
        """Invoke Bedrock model with retry logic"""
        if not self.client:
            return "AI insights unavailable - AWS Bedrock not configured"
        
        try:
            # Format request for Claude 3 Haiku
            request_payload = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": max_tokens,
                "temperature": 0.1,
                "messages": [
                    {
                        "role": "user",
                        "content": [{"type": "text", "text": prompt}]
                    }
                ]
            }
            
            # Convert to JSON
            request_body = json.dumps(request_payload)
            
            # Invoke model
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=request_body,
                contentType='application/json'
            )
            
            # Parse response
            response_body = json.loads(response['body'].read())
            
            # Extract generated text
            if 'content' in response_body and len(response_body['content']) > 0:
                generated_text = response_body['content'][0]['text']
                logger.info("Successfully generated AI insights")
                return generated_text
            else:
                logger.warning("No content in Bedrock response")
                return "AI insights generation failed - no content returned"
                
        except ClientError as e:
            error_code = e.response['Error']['Code']
            logger.error(f"AWS ClientError: {error_code} - {e}")
            
            if error_code == 'AccessDeniedException':
                return "AI insights unavailable - insufficient AWS permissions"
            elif error_code == 'ThrottlingException':
                return "AI insights temporarily unavailable - service busy"
            else:
                return f"AI insights unavailable - AWS error: {error_code}"
                
        except Exception as e:
            logger.error(f"Unexpected error in Bedrock call: {e}")
            return "AI insights temporarily unavailable"
    
    async def generate_tax_insights(self, 
                                  tax_data: Dict[str, Any], 
                                  calculation_result: Dict[str, Any]) -> str:
        """Generate comprehensive tax insights"""
        
        prompt = f"""You are an expert Indian tax consultant specializing in FY 2025-26 tax laws. 
        Analyze this taxpayer's situation and provide actionable insights.

TAXPAYER PROFILE:
- Annual Income: ₹{tax_data.get('income', 0):,}
- Age: {tax_data.get('age', 30)} years
- Tax Regime: {tax_data.get('regime', 'new').upper()} regime
- Employment: {'Salaried' if tax_data.get('is_salaried', True) else 'Self-Employed'}

TAX CALCULATION RESULTS (FY 2025-26):
- Gross Income: ₹{calculation_result.get('gross_income', 0):,}
- Taxable Income: ₹{calculation_result.get('taxable_income', 0):,}
- Final Tax: ₹{calculation_result.get('final_tax', 0):,}
- Effective Rate: {calculation_result.get('effective_rate', 0):.2f}%
- Section 87A Rebate: ₹{calculation_result.get('rebate_87a', 0):,}

UNION BUDGET 2025 KEY CHANGES:
- Basic exemption increased to ₹4 lakh (from ₹3 lakh)
- Section 87A rebate increased to ₹60,000 (up to ₹12 lakh income)
- New 25% slab for ₹20L-₹24L income range
- Standard deduction increased to ₹75,000

Please provide:

1. **TAX OPTIMIZATION STRATEGIES**: 3 specific recommendations with exact amounts
2. **BUDGET 2025 BENEFITS**: How this taxpayer benefits from new changes
3. **INVESTMENT SUGGESTIONS**: Best tax-saving options for next FY
4. **COMPLIANCE REMINDERS**: Key deadlines and requirements

Keep advice practical, specific, and actionable. Use ₹ for amounts."""

        return await self.invoke_model_with_retry(prompt)
    
    def is_available(self) -> bool:
        """Check if AI service is available"""
        return self.client is not None

# Global AI service instance
ai_service = BedrockAIService()
