import csv
import time
import torch
import gc

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

# Path to your CSV file
csv_file_path = "GetPDFUrls.csv"

# Output directory
output_dir = "RegularORC"

process_start = time.time()

# Open the CSV file and process it
with open(csv_file_path, 'r') as file:
    csv_reader = csv.reader(file)

    # Digitalized files using contents of GetPDFUrls.csv
    row_count = 0
    for row in csv_reader:
        url = row[0]
        name = row[1]
        row_count += 1
        if row_count >= 15148: # 
            digitalize_start = time.time()

            try:
                result = converter.convert(url)
                output_path = f"{output_dir}/{name}.md"

                with open(output_path, "w", encoding="utf-8") as file:
                    file.write(result.document.export_to_markdown())

                digitalize_end = time.time()
                digitalize_elapsed_time = digitalize_end - digitalize_start

                print(f"Page {name} successfully digitalized")
                print(f"Stored in {output_path}")
                print(f"File took {digitalize_elapsed_time:.2f} seconds to digitalize")

            except StopIteration:
                print(f"Error: Failed to process {name}. Skipping this file.")
            except Exception as e:
                print(f"Unexpected error processing {name}: {e}")
            
            # Clear GPU memory
            torch.cuda.empty_cache()
            gc.collect()
        
process_end = time.time()
elapsed_time = process_end - process_start

# Convert to days, hours, minutes, and seconds
days = int(elapsed_time // (24 * 3600))  # Total days
elapsed_time %= (24 * 3600)  # Remaining seconds after removing days
hours = int(elapsed_time // 3600)  # Total hours
elapsed_time %= 3600  # Remaining seconds after removing hours
minutes = int(elapsed_time // 60)  # Total minutes
seconds = elapsed_time % 60  # Remaining seconds

print(f"Execution time: {days} days, {hours} hours, {minutes} minutes, and {seconds:.2f} seconds")
