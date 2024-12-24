from pathlib import Path
import time 
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import (
    EasyOcrOptions,
    PdfPipelineOptions,
)
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode

def main():
    input_doc = "https://lamoni.advantage-preservation.com/viewer/GetPdfFile?105894503"
    output_dir = "/Users/jackflickinger/Desktop/GracelandGPT/TestScans"

    pipeline_options = PdfPipelineOptions()
    pipeline_options.do_ocr = True
    pipeline_options.do_table_structure = True
    pipeline_options.table_structure_options.do_cell_matching = True

    # EasyOcrOptions is used because it's the only one that runs on Mac. 
    ocr_options = EasyOcrOptions(force_full_page_ocr=True)
    # ocr_options = TesseractOcrOptions(force_full_page_ocr=True)
    # ocr_options = OcrMacOptions(force_full_page_ocr=True)
    # ocr_options = RapidOcrOptions(force_full_page_ocr=True)
    # ocr_options = TesseractCliOcrOptions(force_full_page_ocr=True)
    pipeline_options.ocr_options = ocr_options
    pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE

    converter = DocumentConverter(
        format_options={
            InputFormat.PDF: PdfFormatOption(
                pipeline_options=pipeline_options,
            )
        }
    )

    start = time.time()
    output_path = f"{output_dir}/test3.md"

    doc = converter.convert(input_doc)
    with open(output_path , "w", encoding="utf-8") as file:
        file.write(doc.document.export_to_markdown())

    end = time.time()
    elapsed_time= end - start
    print(f"file took {elapsed_time:.2f} seconds to digitalize")

if __name__ == "__main__":
    main()
