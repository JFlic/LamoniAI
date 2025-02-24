from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode

import time
pipeline_options = PdfPipelineOptions(do_table_structure=True)
pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE  # use more accurate TableFormer model

doc_converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

start_time = time.time()
page = 1000 # What page you start at

# The range determines how many documents you would like to scan
for i in range(7157):
    source = f"D:\LamoniScans\page_{page}.pdf"  # PDF path or URL
    result = doc_converter.convert(source)
    output_path = f"D:\DigitlizedScans\digitalized_page_{page}.md" # Saved on exterior drive

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(result.document.export_to_markdown())
    
    print(f"page {page} succesfully digitilized")
    print(f"stored in {output_path}")
    
    page += 1

end_time = time.time()
elapsed_time = end_time - start_time

# Convert to days, hours, minutes, and seconds
days = int(elapsed_time // (24 * 3600))  # Total days
elapsed_time %= (24 * 3600)  # Remaining seconds after removing days
hours = int(elapsed_time // 3600)  # Total hours
elapsed_time %= 3600  # Remaining seconds after removing hours
minutes = int(elapsed_time // 60)  # Total minutes
seconds = elapsed_time % 60  # Remaining seconds

print(f"Execution time: {days} days, {hours} hours, {minutes} minutes, and {seconds:.2f} seconds")