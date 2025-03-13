from fastapi import FastAPI
from pydantic import BaseModel
import os
import numpy as np
import psycopg2
from typing import List, Dict, Any
from dotenv import load_dotenv
from pathlib import Path
from sentence_transformers import SentenceTransformer
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever

load_dotenv()

# Constants
EMBED_MODEL_ID = "BAAI/bge-m3"
GEN_MODEL_ID = "mistralai/Mixtral-8x7B-Instruct-v0.1"
HF_TOKEN = os.getenv("HUGGING_FACE_KEY2")
MILVUS_URI = "http://localhost:19530"
TOP_K = 3

# Custom PostgreSQL Retriever
class PostgresRetriever(BaseRetriever):
    """PostgreSQL vector retriever"""
    
    def __init__(self, connection_string: str, embedding_model, top_k: int = 3):
        """Initialize with connection string and embedding model"""
        # Call parent constructor first
        super().__init__()
        # Store parameters as instance variables with proper naming
        self._connection_string = connection_string
        self._embedding_model = embedding_model
        self._top_k = top_k
        
    def _get_relevant_documents(self, query: str, *, run_manager=None) -> List[Document]:
        """Get documents relevant to the query"""
        # Get embedding for the query
        query_embedding = self._embedding_model.embed_query(query)
        
        # Connect to PostgreSQL
        conn = psycopg2.connect(self._connection_string)
        cursor = conn.cursor()
        
        # Perform similarity search using cosine similarity
        cursor.execute("""
            SELECT page_content, source, title, page, chunk_id, doc_type, 
                   1 - (vector <=> %s) as similarity
            FROM document_vectors
            ORDER BY vector <=> %s
            LIMIT %s;
        """, (query_embedding, query_embedding, self._top_k))
        
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        # Convert results to Documents
        documents = []
        for result in results:
            page_content, source, title, page, chunk_id, doc_type, similarity = result
            metadata = {
                "source": source,
                "title": title,
                "page": page,
                "chunk_id": chunk_id,
                "doc_type": doc_type,
                "similarity": float(similarity)  # Add similarity score to metadata
            }
            documents.append(Document(page_content=page_content, metadata=metadata))
        
        return documents

# Standalone function that can be imported by api.py
async def get_query_result(query_request):
    # Initialize embedding model
    embedding = HuggingFaceEmbeddings(model_name=EMBED_MODEL_ID)
    
    # Initialize PostgreSQL retriever
    retriever = PostgresRetriever(
        connection_string=POSTGRES_URI,
        embedding_model=embedding,
        top_k=TOP_K
    )

    llm = HuggingFaceEndpoint(
        huggingfacehub_api_token=HF_TOKEN,
        repo_id=GEN_MODEL_ID
    )

    PROMPT = PromptTemplate.from_template(
        "Context information is below.\n---------------------\n{context}\n---------------------\nGiven the context information and not prior knowledge, answer the query.\nQuery: {input}\nAnswer:\n"
    )

    # Create retrieval and response chain
    question_answer_chain = create_stuff_documents_chain(llm, PROMPT)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    resp_dict = rag_chain.invoke({"input": query_request.query})

    def clip_text(text):
        return f"{text}"

    clipped_answer = clip_text(resp_dict["answer"])

    # Format sources to only include title and page number
    filtered_sources = [
        {
            "title": doc.metadata.get("title", "Unknown"), 
            "page": doc.metadata.get("page", "1"),
            "source": doc.metadata.get("source", "").split("\\")[-1] if doc.metadata.get("source") else "Unknown"
        }
        for doc in resp_dict["context"]
    ]
    print(filtered_sources)
    return {
        "question": query_request.query,
        "answer": clipped_answer,
        "sources": filtered_sources,
    }

# If running this file directly (for testing purposes)
if __name__ == "__main__":
    class QueryRequest(BaseModel):
        query: str
        
    app = FastAPI()

    @app.post("/query/")
    async def query_endpoint(query: QueryRequest):
        return await get_query_result(query)
