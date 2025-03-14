from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_milvus import Milvus
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import PromptTemplate
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from transformers import pipeline
import torch

load_dotenv()
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Constants (you can keep your original constants here)
EMBED_MODEL_ID = "BAAI/bge-m3"
GEN_MODEL_ID = "mistralai/Mistral-7B-Instruct-v0.2"
HF_TOKEN = os.getenv("HUGGING_FACE_KEY2")
MILVUS_URI = "http://localhost:19530"
TOP_K = 3

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/query/")
async def get_query_result(query: QueryRequest):
    # Initialize models and variables (similar to your original code)
    embedding = HuggingFaceEmbeddings(model_name=EMBED_MODEL_ID)
    vectorstore = Milvus(
        collection_name="lamoni_collection",
        embedding_function=embedding,
        connection_args={"uri": MILVUS_URI},
    )

    retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})
    llm = HuggingFaceEndpoint(
        repo_id=GEN_MODEL_ID,
        huggingfacehub_api_token=HF_TOKEN,
    )

    PROMPT = PromptTemplate.from_template(
        """You are an AI assistant at Graceland University. 
        You can provide information, answer questions and perform other tasks as needed.
        \n---------------------\n{context}\n---------------------\n
        Given the context information and not prior knowledge, answer the query.
        If the context is empty say that you don't have any information about the question.
        \nQuery: {input}\nAnswer:\n"""
    )

    # Create retrieval and response chain
    question_answer_chain = create_stuff_documents_chain(llm, PROMPT)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    resp_dict = rag_chain.invoke({"input": query.query})
    clipped_answer = resp_dict["answer"]

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
        "question": query.query,
        "answer": clipped_answer,
        "sources": filtered_sources,
    }
