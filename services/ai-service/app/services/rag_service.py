
"""
RAG Service: Embedding, Storing, and Retrieving Tax Knowledge (Pinecone version)
"""

import pinecone
import numpy as np
from typing import List, Tuple
import boto3
import json
import logging

logger = logging.getLogger(__name__)


class BedrockEmbedder:
    def __init__(self, model_id: str = "amazon.titan-embed-text-v1", region: str = "us-east-1"):
        self.model_id = model_id
        self.region = region
        self.client = boto3.client("bedrock-runtime", region_name=self.region)

    def embed(self, text: str) -> np.ndarray:
        try:
            payload = {
                "inputText": text
            }
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(payload),
                contentType="application/json"
            )
            response_body = json.loads(response["body"].read())
            embedding = response_body["embedding"]
            return np.array(embedding, dtype="float32")
        except Exception as e:
            logger.error(f"Bedrock embedding failed: {e}")
            return np.zeros(1536, dtype="float32")  # Titan returns 1536-dim embeddings


class PineconeVectorStore:
    def __init__(self, dim: int, index_name: str = "tax-rag-index", api_key: str = None, environment: str = None):
        self.dim = dim
        self.index_name = index_name
        self.api_key = api_key or "YOUR_PINECONE_API_KEY"
        self.environment = environment or "YOUR_PINECONE_ENVIRONMENT"
        pinecone.init(api_key=self.api_key, environment=self.environment)
        if self.index_name not in pinecone.list_indexes():
            pinecone.create_index(self.index_name, dimension=self.dim)
        self.index = pinecone.Index(self.index_name)

    def add_document(self, doc_id: str, doc: str, embedding: np.ndarray):
        # Pinecone expects vectors as (id, values, metadata)
        self.index.upsert([(doc_id, embedding.tolist(), {"text": doc})])

    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> List[Tuple[str, float, str]]:
        results = self.index.query(vector=query_embedding.tolist(), top_k=top_k, include_metadata=True)
        return [
            (match["metadata"]["text"], match["score"], match["id"])
            for match in results["matches"]
        ]


# Initialize embedder and Pinecone vector store
embedder = BedrockEmbedder()
vector_store = PineconeVectorStore(dim=1536)

# Example: Add documents from your knowledge base

def add_tax_documents(docs: List[str]):
    for i, doc in enumerate(docs):
        embedding = embedder.embed(doc)
        vector_store.add_document(str(i), doc, embedding)

# Example usage

if __name__ == "__main__":
    # Replace with actual document loading
    docs = ["Sample tax rule 1", "Sample tax rule 2"]
    add_tax_documents(docs)
    query = "What is the exemption limit?"
    query_embedding = embedder.embed(query)
    results = vector_store.search(query_embedding)
    print(results)
