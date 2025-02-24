import requests
from bs4 import BeautifulSoup
import time

# Docling model imports
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, TableFormerMode

# Docling model pipeline configuration 
pipeline_options = PdfPipelineOptions(do_table_structure=True)
pipeline_options.table_structure_options.mode = TableFormerMode.ACCURATE  # use more accurate TableFormer model

# PDF converter pipeline
doc_converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)

# Gets raw iframe tag in order to etract the GetPDF request number
def getsrc(url):
    # Send GET request
    response = requests.get(url)

    if response.status_code == 200:
     
        # Parse the response content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the <iframe> tag with the specific ID
        iframe_tag = soup.find('iframe', id='iObjectpdf')
        
        if iframe_tag:
            # Extract the 'src' attribute
            iframe_src = iframe_tag.get('src')
            return iframe_src
        else:
            print("No <iframe> tag with id='iObjectpdf' found.")
            return None
    else:
        print(f"Request failed with status code: {response.status_code}")
        return None

# Creates the GetPdfFile used for scanning
def CreateGetPDf(raw_iframe):
    # Used to parse raw_iframe
    start = "PubdateId="
    end = "&file"
    Getnumber = raw_iframe.split(start)[1].split(end)[0]
    GetPDfUrl = f"https://lamoni.advantage-preservation.com/viewer/GetPdfFile?{Getnumber}"
    return GetPDfUrl
    

# Creates the name the scan will be saved as
def CreateFileName(raw_iframe):
    # Used to parse raw_iframe
    start = "fn="
    end = "&df="
    fileName = raw_iframe.split(start)[1].split(end)[0]
    return fileName

# Gets the https url to the next url
def getNextArticle(url):
    # Step 1: Fetch the main page and locate the iframe by its id iObjectpdf
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find the iframe by id
        iframe = soup.find("iframe", {"id": "iObjectpdf"})
        
        if iframe:
            # Extract the iframe's src attribute
            iframe_src = iframe.get("src")
            
            # Step 2: Form the full URL of the iframe content
            iframe_url = iframe_src
            if iframe_src.startswith("/"):
                from urllib.parse import urljoin
                iframe_url = urljoin(url, iframe_src)  # Combine base URL and relative path
            
            
            # Step 3: Fetch the iframe's content
            iframe_response = requests.get(iframe_url)
            
            if iframe_response.status_code == 200:
                iframe_soup = BeautifulSoup(iframe_response.text, "html.parser")
                
                iframe_body = iframe_soup.body  # Directly access the <body> tag
                
                if iframe_body:
                    # Step 4: Find the specific <a> element with class "right_arrow2" to click to next page
                    right_arrow_link = iframe_body.find("a", {"class": "right_arrow2"})
                    
                    if right_arrow_link:
                        # Step 5: Create new url to next article
                        href = right_arrow_link.get("href")
                        url = f"https://lamoni.advantage-preservation.com{href}"
                        return url

                    else:
                        print("The <a> element with class 'right_arrow2' was not found.")
                else:
                    print("No <body> tag found in the iframe content.")
            else:
                print("Failed to load iframe content. Status code:", iframe_response.status_code)
        else:
            print("Iframe with id 'iObjectpdf' not found.")
    else:
        print("Failed to fetch the main page. Status code:", response.status_code)


# URL to scrape
url = "https://lamoni.advantage-preservation.com/viewer/?t=39474&i=t&d=01011885-12312020&fn=the_lamoni_chronicle_usa_iowa_lamoni_19330921_english_1&df=1&dt=10&cid=2973"
output_dir = "/Users/jackflickinger/Desktop/GracelandGPT/RawDigitalizedScans"
start_time = time.time()

# The amount of articles that you would like to scan starting at whatever 'url' you chose
articleAmount = 10

for i in range(articleAmount):

    # Creates the file name the scan will be saved as based on url given
    fileName = CreateFileName(url)
    
    # Gets raw iframe tag in order to etract the GetPDF request number
    raw_iframe = getsrc(url)

    # Creates the GetPdfFile used for digitalization
    GetPDFUrl = CreateGetPDf(raw_iframe)

    # Gets the https url to the next url
    nextArticle = getNextArticle(url)

    # Convert PDF to markdown format using doc_convert from Docling pipeline
    digitalize_start = time.time()
    result = doc_converter.convert(GetPDFUrl)
    output_path = f"{output_dir}/{fileName}.md" # Saved to new directory

    with open(output_path , "w", encoding="utf-8") as file:
        file.write(result.document.export_to_markdown())

    digitalize_end = time.time()
    digitalize_elapsed_time= digitalize_end - digitalize_start

    print(f"page {fileName} succesfully digitilized")
    print(f"stored in {output_path}")
    print(f"file took {digitalize_elapsed_time:.2f} seconds to digitalize")
    print("******************************************")

    # Next article becomes current article
    url = nextArticle

end_time = time.time()
elapsed_time = end_time - start_time

# Convert to days, hours, minutes, and seconds
days = int(elapsed_time // (24 * 3600))  # Total days
elapsed_time %= (24 * 3600)  # Remaining seconds after removing days
hours = int(elapsed_time // 3600)  # Total hours
elapsed_time %= 3600  # Remaining seconds after removing hours
minutes = int(elapsed_time // 60)  # Total minutes
seconds = elapsed_time % 60  # Remaining seconds

print(f'Digitilized {articleAmount} articles starting at article "the_lamoni_chronicle_usa_iowa_lamoni_19330921_english_1"')
print(f"Execution time: {days} days, {hours} hours, {minutes} minutes, and {seconds:.2f} seconds")