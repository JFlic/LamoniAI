import time
import torch
import gc
import os

# Docling model imports
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    EasyOcrOptions,
    PdfPipelineOptions,
)

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = False # When True better formating but speed decreases
pipeline_options.do_table_structure = True
pipeline_options.table_structure_options.do_cell_matching = True

# EasyOcrOptions is used because it's the only one that runs on Mac. 
ocr_options = EasyOcrOptions(force_full_page_ocr=False, use_gpu=True) # force_full_page_ocr=True better formating but speed decreases
pipeline_options.ocr_options = ocr_options
pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE

# PDF converter pipeline
converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options = pipeline_options
            )
        }
    )

# Path to folder
input_dir = r"C:\Users\IT Lab VR\Desktop\LamoniAI\GracelandPDFs\Horizons"

# Output directory
output_dir = r"C:\Users\IT Lab VR\Desktop\LamoniAI\GracelandPDFs\GracelandORC"

process_start = time.time()

import time
import torch
import gc
import os

# Process each PDF in the Horizons directory
for index, filename in enumerate(os.listdir(input_dir), start=1):
    if filename.lower().endswith(".pdf"):  # Ensure it's a PDF file
        pdf_path = os.path.join(input_dir, filename)
        name, _ = os.path.splitext(filename)

        # Start Time
        digitalize_start = time.time()
        
        try:
            result = converter.convert(pdf_path)  
            full_markdown = result.document.export_to_markdown()  # Convert the full document
            
            # Split into pages using Markdown page delimiters
            pages = full_markdown.split("\n\n---\n\n")  # Adjust delimiter if needed

            # Save each page separately
            for page_num, page_content in enumerate(pages, start=1):
                output_path = os.path.join(output_dir, f"{name}_page_{page_num}.md")

                with open(output_path, "w", encoding="utf-8") as file:
                    file.write(page_content.strip())  # Remove extra spaces

                print(f"Saved {name} - Page {page_num} to {output_path}")

            digitalize_end = time.time()
            digitalize_elapsed_time = digitalize_end - digitalize_start
            
            print(f"{name} successfully digitalized into {len(pages)} pages")
            print(f"File took {digitalize_elapsed_time:.2f} seconds to digitalize")
        
        except StopIteration:
            print(f"Error: Failed to process {name}. Skipping this file.")
        except Exception as e:
            print(f"Unexpected error processing {name}: {e}")
        
        # Clear GPU memory after each PDF
        torch.cuda.empty_cache()
        gc.collect()

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

print(f"Execution time: {days} days, {hours} hours, {minutes} minutes, and {seconds:.2f} seconds")
