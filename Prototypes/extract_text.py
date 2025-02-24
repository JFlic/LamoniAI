import os
from docling.document_converter import DocumentConverter

# Initialize the converter
converter = DocumentConverter()

def extract_texts_from_pdfs(pdf_directory, output_directory):
    """Extracts text from PDFs and saves them as Markdown files."""
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            file_path = os.path.join(pdf_directory, filename)
            output_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}.md")

            try:
                result = converter.convert(file_path)
                extracted_text = result.document.export_to_markdown()

                with open(output_path, "w", encoding="utf-8") as file:
                    file.write(extracted_text)

                print(f"✅ Extracted and saved: {output_path}")

            except Exception as e:
                print(f"❌ Error processing {file_path}: {e}")

# Run extraction
if __name__ == "__main__":
    pdf_directory = r"C:\Users\IT Lab VR\Desktop\LamoniAI\GracelandPDFs\Horizons"  # Folder containing PDFs
    output_directory = r"C:\Users\IT Lab VR\Desktop\LamoniAI\GracelandPDFs\ExtractedText"  # Folder to save extracted text
    extract_texts_from_pdfs(pdf_directory, output_directory)
