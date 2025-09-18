
"""
RAG Service: Embedding, Storing, and Retrieving Tax Knowledge (In-Memory version)
"""

import numpy as np
from typing import List, Tuple
import boto3
import json
import logging
import os
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)
load_dotenv()


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
        self.dim = dim
        self.documents = []
        self.embeddings = []
        self.doc_ids = []

    def add_document(self, doc_id: str, doc: str, embedding: np.ndarray):
        self.doc_ids.append(doc_id)
        self.documents.append(doc)
        self.embeddings.append(embedding)

    def search(self, query_embedding: np.ndarray, top_k: int = 3) -> List[Tuple[str, float, str]]:
        if not self.embeddings:
            return []
        
        # Convert to numpy array for similarity calculation
        embeddings_matrix = np.array(self.embeddings)
        query_embedding = query_embedding.reshape(1, -1)
        
        # Calculate cosine similarity
        similarities = cosine_similarity(query_embedding, embeddings_matrix)[0]
        
        # Get top_k most similar documents
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            results.append((
                self.documents[idx],  # text
                float(similarities[idx]),  # score
                self.doc_ids[idx]  # id
            ))
        
        return results


# Initialize embedder and simple vector store
embedder = BedrockEmbedder()
vector_store = SimpleVectorStore(dim=1536)

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
