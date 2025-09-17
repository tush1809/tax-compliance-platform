"""
RAG Service: Embedding, Storing, and Retrieving Tax Knowledge
"""

import faiss
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

class SimpleVectorStore:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatL2(dim)
        self.documents = []
        self.embeddings = []

    def add_document(self, doc: str, embedding: np.ndarray):
        self.documents.append(doc)
        self.embeddings.append(embedding)
        self.index.add(np.array([embedding]).astype('float32'))

    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> List[Tuple[str, float]]:
        D, I = self.index.search(np.array([query_embedding]).astype('float32'), top_k)
        results = [(self.documents[i], float(D[0][idx])) for idx, i in enumerate(I[0])]
        return results

# Initialize embedder and vector store
embedder = BedrockEmbedder()
vector_store = SimpleVectorStore(dim=1536)

# Example: Add documents from your knowledge base
def add_tax_documents(docs: List[str]):
    for doc in docs:
        embedding = embedder.embed(doc)
        vector_store.add_document(doc, embedding)

# Example usage
if __name__ == "__main__":
    # Replace with actual document loading
    docs = ["Sample tax rule 1", "Sample tax rule 2"]
    add_tax_documents(docs)
    query = "What is the exemption limit?"
    query_embedding = embedder.embed(query)
    results = vector_store.search(query_embedding)
    print(results)
