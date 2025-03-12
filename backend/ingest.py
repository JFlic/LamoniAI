import os
import glob
import json
import time
from pathlib import Path
from dotenv import load_dotenv
import psycopg2
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_docling.loader import ExportType
from langchain_docling import DoclingLoader
from docling.chunking import HybridChunker
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document
from huggingface_hub import login

process_start = time.time()

load_dotenv()
HF_TOKEN = os.getenv("HUGGING_FACE_KEY2")
login(token=HF_TOKEN)
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Constants
HORIZONS_DIR = r"C:\Users\IT Lab VR\Desktop\LamoniAI\backend\TempDocumentStore"
EMBED_MODEL_ID = "BAAI/bge-m3"
EXPORT_TYPE = ExportType.DOC_CHUNKS
POSTGRES_URI = "postgresql://postgres:RaG32!happyL1fe@localhost:5432/postgres"  # Adjust as needed

# Function to create the table if it doesn't exist with improved error handling
def create_table_if_not_exists(conn):
    cursor = conn.cursor()
    
    # Create vector extension if it doesn't exist
    try:
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        print("Vector extension created or already exists.")
    except Exception as e:
        print(f"Error creating vector extension: {e}")
        print("Please create the extension manually in the correct database.")
        print("Run: docker exec -it timescaledb psql -U postgres -d postgres -c \"CREATE EXTENSION vector;\"")
        conn.rollback()
        raise
    
    # Create table with vector column
    try:
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS document_vectors (
            id SERIAL PRIMARY KEY,
            page_content TEXT,
            source TEXT,
            title TEXT,
            page INT,
            chunk_id TEXT,
            doc_type TEXT,
            vector vector
        );
        """)
        print("Table document_vectors created or already exists.")
    except Exception as e:
        print(f"Error creating table: {e}")
        conn.rollback()
        raise
    
    # Try creating the index, but don't fail if it's not possible
    try:
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS document_vectors_vector_idx 
        ON document_vectors 
        USING ivfflat (vector vector_cosine_ops)
        WITH (lists = 100);
        """)
        print("Index created successfully.")
    except Exception as e:
        print(f"Warning: ivfflat index creation failed: {e}")
        print("This might be due to missing ivfflat support in this version of pgvector.")
        print("The application will still work, but similarity searches will be slower.")
        # Important: Don't rollback here, we want to keep the table even if index fails
        conn.commit()  # Commit the table creation even if index fails
        
        # Try creating a simpler index instead
        try:
            cursor.execute("""
            CREATE INDEX IF NOT EXISTS document_vectors_vector_idx 
            ON document_vectors 
            USING hnsw (vector vector_cosine_ops);
            """)
            print("HNSW index created as fallback.")
        except Exception as e2:
            print(f"Warning: HNSW index creation also failed: {e2}")
            try:
                # Last resort - try creating an index without specifying method
                cursor.execute("""
                CREATE INDEX IF NOT EXISTS document_vectors_vector_idx 
                ON document_vectors (vector);
                """)
                print("Basic index created as fallback.")
            except Exception as e3:
                print(f"Warning: Basic index creation also failed: {e3}")
                print("Continuing without vector index. Searches will be slow.")
    
    conn.commit()
    cursor.close()
    
    # Verify table was actually created
    verify_cursor = conn.cursor()
    verify_cursor.execute("SELECT to_regclass('document_vectors');")
    table_exists = verify_cursor.fetchone()[0]
    verify_cursor.close()
    
    if not table_exists:
        raise Exception("Table creation appeared to succeed but the table doesn't exist. Check PostgreSQL logs.")
    
    print("Table verification successful, document_vectors exists.")

# Function to get connection to Postgres
def get_postgres_connection():
    try:
        conn = psycopg2.connect(POSTGRES_URI)
        print("Successfully connected to PostgreSQL database")
        return conn
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")
        raise

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

# Main execution starts here
try:
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

    # Connect to PostgreSQL and ensure the table exists
    conn = get_postgres_connection()
    create_table_if_not_exists(conn)

    # Prepare to insert data into PostgreSQL
    cursor = conn.cursor()

    for i in range(0, total_docs, batch_size):
        end_idx = min(i + batch_size, total_docs)
        batch = all_splits[i:end_idx]
        print(f"Processing batch {i//batch_size + 1}/{(total_docs + batch_size - 1)//batch_size}: documents {i} to {end_idx-1}")
        
        successful_inserts = 0
        for doc in batch:
            try:
                # Assuming you are extracting the vector embedding from the `doc` (you need to adapt this to how you handle embeddings)
                vector = embedding.embed_documents([doc.page_content])[0]  # Embedding the document content
                page_content = doc.page_content
                # Extract metadata for the document
                metadata = doc.metadata
                source = metadata.get('source', '')
                title = metadata.get('title', '')
                page = metadata.get('page', 0)
                chunk_id = metadata.get('chunk_id', '')
                doc_type = metadata.get('doc_type', '')

                # Insert the document into the `document_vectors` table
                cursor.execute("""
                INSERT INTO document_vectors (page_content, source, title, page, chunk_id, doc_type, vector)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (page_content, source, title, page, chunk_id, doc_type, vector))
                
                successful_inserts += 1
            except Exception as e:
                print(f"Error inserting document: {e}")
                # Continue with the next document instead of failing the entire batch
                conn.rollback()
                continue
        
        # Commit the batch to the database
        try:
            conn.commit()
            print(f"Successfully inserted {successful_inserts} documents in this batch")
        except Exception as e:
            print(f"Error committing batch: {e}")
            conn.rollback()

    cursor.close()
    conn.close()

    print("Data ingestion complete. Chunks stored in PostgreSQL.")
    milvus_end = time.time()
    milvus_time = milvus_end - milvus_start

    # Convert to days, hours, minutes, and seconds
    days = int(milvus_time // (24 * 3600))
    milvus_time %= (24 * 3600)
    hours = int(milvus_time // 3600)
    milvus_time %= 3600
    minutes = int(milvus_time // 60)
    seconds = milvus_time % 60

    print(f"PostgreSQL ingestion time: {days} days, {hours} hours, {minutes} minutes, and {seconds:.2f} seconds")

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

except Exception as e:
    print(f"An error occurred during execution: {e}")
    # If we have a connection object in this scope, close it
    if 'conn' in locals() and conn:
        conn.close()