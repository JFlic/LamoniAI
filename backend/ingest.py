import os
import glob
import json
import time
from pathlib import Path
from dotenv import load_dotenv
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_milvus import Milvus
from langchain_docling.loader import ExportType
from langchain_docling import DoclingLoader
from docling.chunking import HybridChunker
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document

process_start = time.time()

load_dotenv()
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Constants
HORIZONS_DIR = r"C:\Users\IT Lab VR\Desktop\LamoniAI\backend\TempDocumentStore"
EMBED_MODEL_ID = "BAAI/bge-m3"
EXPORT_TYPE = ExportType.DOC_CHUNKS
MILVUS_URI = "http://localhost:19530"  # Adjust as needed

# Function to trim metadata to prevent oversize issues
def trim_metadata(docs):
    trimmed_docs = []
    for doc in docs:
        # Create a simplified metadata dictionary with only essential fields
        simplified_metadata = {
            "source": doc.metadata.get("source", ""),
            "title": doc.metadata.get("title", "")[:1000] if doc.metadata.get("title") else "",  # Limit title length
            "page": doc.metadata.get("page", 0),
            "chunk_id": doc.metadata.get("chunk_id", ""),
        }
        
        # If you need to preserve any special fields from dl_meta, extract just what you need
        if "dl_meta" in doc.metadata and isinstance(doc.metadata["dl_meta"], dict):
            # Extract only essential information from dl_meta if needed
            simplified_metadata["doc_type"] = doc.metadata["dl_meta"].get("doc_type", "")
            
        # Create a new document with the simplified metadata
        trimmed_doc = Document(
            page_content=doc.page_content,
            metadata=simplified_metadata
        )
        trimmed_docs.append(trimmed_doc)
    
    return trimmed_docs

# Gather all PDF and Markdown files
pdf_files = glob.glob(os.path.join(HORIZONS_DIR, "*.pdf"))
md_files = glob.glob(os.path.join(HORIZONS_DIR, "*.md"))

print(f"Processing {len(pdf_files)} PDFs and {len(md_files)} Markdown files from the Horizons directory")

# Load and chunk documents
all_splits = []

# Process Markdown files
for file in md_files:
    print(f"Loading Markdown: {Path(file).name}")
    loader = DoclingLoader(
        file_path=[file],
        export_type=EXPORT_TYPE,
        chunker=HybridChunker(tokenizer=EMBED_MODEL_ID),
    )
    docs = loader.load()
    # Trim metadata to prevent oversize issues
    trimmed_docs = trim_metadata(docs)
    all_splits.extend(trimmed_docs)

# Process PDF files
for file in pdf_files:
    print(f"Loading PDF: {Path(file).name}")
    loader = DoclingLoader(
        file_path=[file],
        export_type=EXPORT_TYPE,
        chunker=HybridChunker(tokenizer=EMBED_MODEL_ID),
    )
    docs = loader.load()
    # Trim metadata to prevent oversize issues
    trimmed_docs = trim_metadata(docs)
    all_splits.extend(trimmed_docs)

print(f"Total document chunks created: {len(all_splits)}")

milvus_start = time.time()

# Initialize embedding and vector store
embedding = HuggingFaceEmbeddings(model_name=EMBED_MODEL_ID)

# Process in smaller batches to avoid oversize issues
batch_size = 30
total_docs = len(all_splits)
vectorstore = None

for i in range(0, total_docs, batch_size):
    end_idx = min(i + batch_size, total_docs)
    batch = all_splits[i:end_idx]
    print(f"Processing batch {i//batch_size + 1}/{(total_docs + batch_size - 1)//batch_size}: documents {i} to {end_idx-1}")
    
    if vectorstore is None:
        # Create the vectorstore with the first batch
        vectorstore = Milvus.from_documents(
            documents=batch,
            embedding=embedding,
            collection_name="lamoni_collection",
            connection_args={"uri": MILVUS_URI},
            index_params={"index_type": "FLAT", "metric_type": "COSINE"},
            drop_old=(i == 0),  # Only drop old collection on first batch
        )
    else:
        # Add subsequent batches to the existing vectorstore
        vectorstore.add_documents(
            documents=batch,
            embedding=embedding,
            collection_name="lamoni_collection",
            connection_args={"uri": MILVUS_URI},
            index_params={"index_type": "FLAT", "metric_type": "COSINE"},
            drop_old=(i == 0),  # Only drop old collection on first batch
        )

print("Data ingestion complete. Chunks stored in Milvus.")
milvus_end = time.time()
milvus_time = milvus_end - milvus_start

# Convert to days, hours, minutes, and seconds
days = int(milvus_time // (24 * 3600))
milvus_time %= (24 * 3600)
hours = int(milvus_time // 3600)
milvus_time %= 3600
minutes = int(milvus_time // 60)
seconds = milvus_time % 60

print(f"Milvus ingestion time: {days} days, {hours} hours, {minutes} minutes, and {seconds:.2f} seconds")

# End Time
process_end = time.time()
elapsed_time = process_end - process_start

# Convert to days, hours, minutes, and seconds
days = int(elapsed_time // (24 * 3600))
elapsed_time %= (24 * 3600)
hours = int(elapsed_time // 3600)
elapsed_time %= 3600
minutes = int(elapsed_time // 60)
seconds = elapsed_time % 60

print(f"Total process execution time: {days} days, {hours} hours, {minutes} minutes, and {seconds:.2f} seconds")