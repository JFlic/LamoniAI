import os
import json
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

# Constants
EMBED_MODEL_ID = "BAAI/bge-m3"
GEN_MODEL_ID = "mistralai/Mixtral-8x7B-Instruct-v0.1"
HF_TOKEN = os.getenv("HUGGING_FACE_KEY")
MILVUS_URI = "http://localhost:19530"
TOP_K = 3
QUESTION = "Tell me about the Burlington system"

PROMPT = PromptTemplate.from_template(
    "Context information is below.\n---------------------\n{context}\n---------------------\nGiven the context information and not prior knowledge, answer the query.\nQuery: {input}\nAnswer:\n"
)

# Load vector store
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

# Create retrieval and response chain
question_answer_chain = create_stuff_documents_chain(llm, PROMPT)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)
resp_dict = rag_chain.invoke({"input": QUESTION})

def clip_text(text, threshold=100):
    return f"{text[:threshold]}..." if len(text) > threshold else text

clipped_answer = clip_text(resp_dict["answer"], threshold=1000)
print(f"Question:\n{resp_dict['input']}\n\nAnswer:\n{clipped_answer}")

# Print sources
for i, doc in enumerate(resp_dict["context"]):
    print()
    print(f"Source {i+1}:")
    print(f"  text: {json.dumps(clip_text(doc.page_content, threshold=500))}")
    
    dl_meta = doc.metadata.get("dl_meta", {})
    article_name = Path(dl_meta["origin"]["filename"]).stem if "origin" in dl_meta and "filename" in dl_meta["origin"] else "Unknown Article"
    
    page_number = "Unknown Page"
    if "doc_items" in dl_meta and dl_meta["doc_items"]:
        prov_data = dl_meta["doc_items"][0].get("prov", [])
        if prov_data:
            page_number = prov_data[0].get("page_no", "Unknown Page")

    print(f"  Article Name: {article_name}")
    print(f"  Page Number: {page_number}")
