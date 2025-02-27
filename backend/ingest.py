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

# Gather all PDF and Markdown files
pdf_files = glob.glob(os.path.join(HORIZONS_DIR, "*.pdf"))
md_files = glob.glob(os.path.join(HORIZONS_DIR, "*.md"))

print(f"Processing {len(pdf_files)} PDFs and {len(md_files)} Markdown files from the Horizons directory")

# Load and chunk documents
all_splits = []

# Process Markdown files
markdown_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[("#", "Header_1"), ("##", "Header_2"), ("###", "Header_3")]
)

for file in md_files:
    print(f"Loading Markdown: {Path(file).name}")
    loader = DoclingLoader(
        file_path=[file],
        export_type=EXPORT_TYPE,
        chunker=HybridChunker(tokenizer=EMBED_MODEL_ID),
    )
    docs = loader.load()

    # create a dictionary object from GetPDFUrls.csv that will store the keys as markdown file names and source urls as values
    # for doc in docs:
    #     full_path =doc.metadata["source"]
    #     filename = os.path.basename(full_path)
    #     print(filename[:-3])

    # all_splits.extend(docs)

# Process PDF files
for file in pdf_files:
    print(f"Loading PDF: {Path(file).name}")
    loader = DoclingLoader(
        file_path=[file],
        export_type=EXPORT_TYPE,
        chunker=HybridChunker(tokenizer=EMBED_MODEL_ID),
    )
    docs = loader.load()

    
    all_splits.extend(docs)

print(f"Total document chunks created: {len(all_splits)}")

milvus_start = time.time()

# Initialize embedding and vector store
embedding = HuggingFaceEmbeddings(model_name=EMBED_MODEL_ID)
vectorstore = Milvus.from_documents(
    documents=all_splits,
    embedding=embedding,
    collection_name="lamoni_collection",
    connection_args={"uri": MILVUS_URI},
    index_params={"index_type": "FLAT", "metric_type": "COSINE"},
    drop_old=True,
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

print(f"Total Ingestion Execution time: {days} days, {hours} hours, {minutes} minutes, and {seconds:.2f} seconds")

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

print(f"Total Ingestion Execution time: {days} days, {hours} hours, {minutes} minutes, and {seconds:.2f} seconds")