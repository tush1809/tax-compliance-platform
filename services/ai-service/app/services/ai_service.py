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


# --- Refactored Classes ---

class ClientManager:
    def __init__(self, region: str):
        self.region = region
        self.client = self._initialize_client()

    def _initialize_client(self):
        try:
            client = boto3.client('bedrock-runtime', region_name=self.region)
            logger.info("AWS Bedrock client initialized successfully")
            return client
        except NoCredentialsError:
            logger.error("AWS credentials not found. AI features will be disabled.")
            return None
        except Exception as e:
            logger.error(f"Failed to initialize AWS Bedrock client: {e}")
            return None

    def is_available(self):
        return self.client is not None

class PromptBuilder:
    @staticmethod
    def build_tax_insight_prompt(tax_data: Dict[str, Any], calculation_result: Dict[str, Any]) -> str:
        return f"""You are an expert Indian tax consultant specializing in FY 2025-26 tax laws. 
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

class ModelInvoker:
    def __init__(self, client, model_id: str):
        self.client = client
        self.model_id = model_id

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        retry=retry_if_exception_type(ClientError)
    )
    async def invoke(self, prompt: str, max_tokens: int = 2000) -> str:
        if not self.client:
            return "AI insights unavailable - AWS Bedrock not configured"
        try:
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
            request_body = json.dumps(request_payload)
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=request_body,
                contentType='application/json'
            )
            response_body = json.loads(response['body'].read())
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

class TaxInsightService:
    def __init__(self, region: str, model_id: str):
        self.client_manager = ClientManager(region)
        self.model_invoker = ModelInvoker(self.client_manager.client, model_id)

    async def generate_tax_insights(self, tax_data: Dict[str, Any], calculation_result: Dict[str, Any]) -> str:
        prompt = PromptBuilder.build_tax_insight_prompt(tax_data, calculation_result)
        return await self.model_invoker.invoke(prompt)

    def is_available(self):
        return self.client_manager.is_available()

# Global AI service instance
ai_service = TaxInsightService(region="us-east-1", model_id="anthropic.claude-3-haiku-20240307-v1:0")
