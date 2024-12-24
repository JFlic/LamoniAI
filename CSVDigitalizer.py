import csv
import time

# Docling model imports
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    EasyOcrOptions,
    PdfPipelineOptions,
)

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode
pipeline_options = PdfPipelineOptions()
pipeline_options.do_ocr = True
pipeline_options.do_table_structure = True
pipeline_options.table_structure_options.do_cell_matching = True

# EasyOcrOptions is used because it's the only one that runs on Mac. 
ocr_options = EasyOcrOptions(force_full_page_ocr=True)
pipeline_options.ocr_options = ocr_options
pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE

# PDF converter pipeline
converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
            )
        }
    )

# Path to your CSV file
csv_file_path = "GetPDFUrls.csv"

# Output directory
output_dir = "/Users/jackflickinger/Desktop/GracelandGPT/RawDigitalizedScans"

process_start = time.time()

# Open the CSV file and process it
with open(csv_file_path, 'r') as file:
    csv_reader = csv.reader(file)

    # Process only the first 10 rows
    # just remove the row_count if statement stuff and you can digitalize the whole csv file. 
    row_count = 0
    for row in csv_reader:
        if row_count <= 17:
            row_count += 1
        elif row_count > 17 and row_count <= 100:
            url = row[0]
            name = row[1]
            row_count += 1

            digitalize_start = time.time()
            result = converter.convert(url)
            output_path = f"{output_dir}/{name}.md" # Saved to new directory

            with open(output_path , "w", encoding="utf-8") as file:
                file.write(result.document.export_to_markdown())

            digitalize_end = time.time()
            digitalize_elapsed_time = digitalize_end - digitalize_start

            print(f"page {name} succesfully digitilized")
            print(f"stored in {output_path}")
            print(f"file took {digitalize_elapsed_time:.2f} seconds to digitalize")
            print("******************************************")

        else:
            break

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