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

load_dotenv()
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Constants (you can keep your original constants here)
EMBED_MODEL_ID = "BAAI/bge-m3"
GEN_MODEL_ID = "mistralai/Mixtral-8x7B-Instruct-v0.1"
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
        "Context information is below.\n---------------------\n{context}\n---------------------\nGiven the context information and not prior knowledge, answer the query.\nQuery: {input}\nAnswer:\n"
    )

    # Create retrieval and response chain
    question_answer_chain = create_stuff_documents_chain(llm, PROMPT)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    resp_dict = rag_chain.invoke({"input": query.query})

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
        "question": query.query,
        "answer": clipped_answer,
        "sources": filtered_sources,
    }
