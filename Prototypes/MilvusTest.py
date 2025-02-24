import os
import glob
from pathlib import Path
import json
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_milvus import Milvus

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_docling.loader import ExportType
from langchain_docling import DoclingLoader
from docling.chunking import HybridChunker

from huggingface_hub import login

# RAG
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_huggingface import HuggingFaceEndpoint

os.environ["TOKENIZERS_PARALLELISM"] = "false"

HF_TOKEN = os.getenv("HUGGING_FACE_KEY")
# Update to use all PDFs in the Horizons directory
HORIZONS_DIR = r"Horizons"
FILE_PATH = glob.glob(os.path.join(HORIZONS_DIR, "*.pdf"))
EMBED_MODEL_ID = "BAAI/bge-m3"
GEN_MODEL_ID = "mistralai/Mixtral-8x7B-Instruct-v0.1"
EXPORT_TYPE = ExportType.DOC_CHUNKS
QUESTION = "Tell me about North Park in Lamoni"
PROMPT = PromptTemplate.from_template(
    "Context information is below.\n---------------------\n{context}\n---------------------\nGiven the context information and not prior knowledge, answer the query.\nQuery: {input}\nAnswer:\n",
)
TOP_K = 3

print(f"Processing {len(FILE_PATH)} PDF files from the Horizons directory")

# Load all documents into docling loader
all_splits = []
for file in FILE_PATH:
    print(f"Loading: {Path(file).name}")
    loader = DoclingLoader(
        file_path=[file],  # DoclingLoader expects a list
        export_type=EXPORT_TYPE,
        chunker=HybridChunker(tokenizer=EMBED_MODEL_ID),
    )
    
    docs = loader.load()
    
    if EXPORT_TYPE == ExportType.DOC_CHUNKS:
        splits = docs
    
    # This is for if you want to Export the chunks in markdown
    elif EXPORT_TYPE == ExportType.MARKDOWN:
        from langchain_text_splitters import MarkdownHeaderTextSplitter
        
        splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "Header_1"),
                ("##", "Header_2"),
                ("###", "Header_3"),
            ],
        )
        splits = [split for doc in docs for split in splitter.split_text(doc.page_content)]
    else:
        raise ValueError(f"Unexpected export type: {EXPORT_TYPE}")
    
    all_splits.extend(splits)

print(f"Total document chunks created: {len(all_splits)}")

# Sample the first document for inspection
if all_splits:
    print("Sample of first document chunk:")
    print(f"- {all_splits[0].page_content[:300]}...")
    print("-" * 80)

# Set up vector store with all documents
embedding = HuggingFaceEmbeddings(model_name=EMBED_MODEL_ID)
milvus_uri = "http://localhost:19530"  # or set as needed

vectorstore = Milvus.from_documents(
    documents=all_splits,
    embedding=embedding,
    collection_name="lamoni_collection",
    connection_args={"uri": milvus_uri},
    index_params={
        "index_type": "FLAT",
        "metric_type": "COSINE"
    },
    drop_old=True,
)

retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})
llm = HuggingFaceEndpoint(
    repo_id=GEN_MODEL_ID,
    huggingfacehub_api_token=HF_TOKEN,
)

def clip_text(text, threshold=100):
    return f"{text[:threshold]}..." if len(text) > threshold else text

question_answer_chain = create_stuff_documents_chain(llm, PROMPT)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)
resp_dict = rag_chain.invoke({"input": QUESTION})

clipped_answer = clip_text(resp_dict["answer"], threshold=1000)
print(f"Question:\n{resp_dict['input']}\n\nAnswer:\n{clipped_answer}")

for i, doc in enumerate(resp_dict["context"]):
    print()
    print(f"Source {i+1}:")
    print(f"  text: {json.dumps(clip_text(doc.page_content, threshold=500))}")
    
    # Extract metadata safely
    dl_meta = doc.metadata.get("dl_meta", {})
    
    # Extract article name from the PDF filename
    article_name = "Unknown Article"
    if "origin" in dl_meta and "filename" in dl_meta["origin"]:
        article_name = Path(dl_meta["origin"]["filename"]).stem  # Remove file extension
    
    # Get page number
    page_number = "Unknown Page"
    if "doc_items" in dl_meta and dl_meta["doc_items"]:
        prov_data = dl_meta["doc_items"][0].get("prov", [])
        if prov_data:
            page_number = prov_data[0].get("page_no", "Unknown Page")
    
    print(f"  Article Name: {article_name}")
    print(f"  Page Number: {page_number}")
