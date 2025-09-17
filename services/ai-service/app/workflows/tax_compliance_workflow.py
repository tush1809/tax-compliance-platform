
from langgraph.graph import StateGraph
from ..services.rag_service import vector_store, embedder
from ..agents.tax_calculator.calculator_fy2025 import (
    calculate_new_regime_tax_fy2025,
    calculate_old_regime_tax_fy2025,
    TaxCalculationInput
)

# Example: Define a simple workflow for tax compliance with RAG
class TaxComplianceState:
    def __init__(self, user_data=None):
        self.user_data = user_data or {}
        self.calculation_result = None
        self.validation_result = None
        self.retrieved_context = None

# RAG node: Retrieve relevant context from knowledge base
def retrieve_context(state: TaxComplianceState):
    query = state.user_data.get('query', 'tax compliance rules')
    query_embedding = embedder.embed(query)
    results = vector_store.search(query_embedding, top_k=3)
    state.retrieved_context = '\n'.join([doc for doc, _ in results])
    return state

# Define nodes (steps)
def calculate_tax(state: TaxComplianceState):
    user = state.user_data
    calc_input = TaxCalculationInput(
        gross_income=user.get('income', 0),
        age=user.get('age', 30),
        regime=user.get('regime', 'new'),
        is_salaried=user.get('is_salaried', True),
        deductions_80c=user.get('deductions_80c', 0),
        health_insurance_premium=user.get('health_insurance_premium', 0)
    )
    if calc_input.regime == 'new':
        state.calculation_result = calculate_new_regime_tax_fy2025(calc_input)
    else:
        state.calculation_result = calculate_old_regime_tax_fy2025(calc_input)
    return state

def validate_rules(state: TaxComplianceState):
    # Placeholder for rule validation logic
    state.validation_result = {'compliance': True}
    return state

# Build the workflow graph
graph = StateGraph(TaxComplianceState)
graph.add_node('retrieve_context', retrieve_context)
graph.add_node('calculate_tax', calculate_tax)
graph.add_node('validate_rules', validate_rules)
graph.add_edge('retrieve_context', 'calculate_tax')
graph.add_edge('calculate_tax', 'validate_rules')
graph.set_entry_point('retrieve_context')
workflow = graph.compile()

# Example usage
def run_workflow(user_data):
    state = TaxComplianceState(user_data)
    final_state = workflow.invoke(state)
    return {
        'tax': final_state.calculation_result,
        'validation': final_state.validation_result,
        'retrieved_context': final_state.retrieved_context
    }
