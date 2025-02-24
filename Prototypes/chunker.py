import os
import json
from tqdm import tqdm
from docling.document_converter import DocumentConverter
from docling.chunking import HybridChunker

# Define the directory containing the PDFs
horizons_dir = r"C:\Users\IT Lab VR\Desktop\LamoniAI\GracelandPDFs\Horizons"
output_file = r"C:\Users\IT Lab VR\Desktop\LamoniAI\GracelandPDFs\horizons_chunks.json"

# Initialize chunker
chunker = HybridChunker(
    tokenizer="BAAI/bge-m3",
    max_tokens=8192,
    merge_peers=True
)

conv_res = DocumentConverter()

# List all PDF files in the directory
pdf_files = [f for f in os.listdir(horizons_dir) if f.endswith(".pdf")]

all_chunks = {}

# Use tqdm to display progress
for pdf_file in tqdm(pdf_files, desc="Processing PDFs", unit="file"):
    pdf_path = os.path.join(horizons_dir, pdf_file)

    # Convert the PDF to text
    result = conv_res.convert(pdf_path)
    doc = result.document

    # Chunk the document
    chunk_iter = chunker.chunk(doc)
    chunks = list(chunk_iter)

    # Store chunks with filename as key
    all_chunks[pdf_file] = [str(chunk) for chunk in chunks]

# Save the chunks to a JSON file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_chunks, f, indent=4)

print(f"All chunks saved to {output_file}")
