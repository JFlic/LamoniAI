import os
import glob
import json
from pathlib import Path
from dotenv import load_dotenv
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_milvus import Milvus
from langchain_docling.loader import ExportType
from langchain_docling import DoclingLoader
from docling.chunking import HybridChunker

load_dotenv()
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Constants
HORIZONS_DIR = r"C:\Users\IT Lab VR\Desktop\LamoniAI\GracelandPDFs\Horizons"
FILE_PATH = glob.glob(os.path.join(HORIZONS_DIR, "*.pdf"))
EMBED_MODEL_ID = "BAAI/bge-m3"
EXPORT_TYPE = ExportType.DOC_CHUNKS
MILVUS_URI = "http://localhost:19530"  # Adjust as needed

print(f"Processing {len(FILE_PATH)} PDF files from the Horizons directory")

# Load and chunk documents
all_splits = []
for file in FILE_PATH:
    print(f"Loading: {Path(file).name}")
    loader = DoclingLoader(
        file_path=[file],
        export_type=EXPORT_TYPE,
        chunker=HybridChunker(tokenizer=EMBED_MODEL_ID),
    )
    docs = loader.load()
    splits = docs if EXPORT_TYPE == ExportType.DOC_CHUNKS else []
    
    all_splits.extend(splits)

print(f"Total document chunks created: {len(all_splits)}")

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
