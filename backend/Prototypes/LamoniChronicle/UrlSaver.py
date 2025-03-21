import requests
from bs4 import BeautifulSoup
import time
import csv

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
    # Fetch the main page and locate the iframe by its id iObjectpdf
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Find the iframe by id
        iframe = soup.find("iframe", {"id": "iObjectpdf"})
        
        if iframe:
            # Extract the iframe's src attribute
            iframe_src = iframe.get("src")
            
            # Form the full URL of the iframe content
            iframe_url = iframe_src
            if iframe_src.startswith("/"):
                from urllib.parse import urljoin
                iframe_url = urljoin(url, iframe_src)  # Combine base URL and relative path
            
            
            # Fetch the iframe's content
            iframe_response = requests.get(iframe_url)
            
            if iframe_response.status_code == 200:
                iframe_soup = BeautifulSoup(iframe_response.text, "html.parser")
                
                iframe_body = iframe_soup.body  # Directly access the <body> tag
                
                if iframe_body:
                    # Find the specific <a> element with class "right_arrow2" to click to next page
                    right_arrow_link = iframe_body.find("a", {"class": "right_arrow2"})
                    
                    if right_arrow_link:
                        # Create new url to next article
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


# Function to add multiple rows to a CSV file
def append_to_csv(file_name, data):
    # Open the file in append mode
    with open(file_name, 'a', newline='') as csvfile:
        # Define the fieldnames (column headers)
        fieldnames = ['url', 'name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Write rows of data
        writer.writerows(data)

# URL to scrape
url = "https://lamoni.advantage-preservation.com/viewer/?t=39474&i=t&by=1904&bdd=1900&d=01011885-12312020&fn=the_lamoni_chronicle_usa_iowa_lamoni_19040128_english_3&df=41&dt=50&cid=2973"

# File that Getpdf info will be in
csv_file = 'GetPDFUrls.csv'

start_time = time.time()

# The amount of articles that you would like to save starting at whatever 'url' you chose
articleAmount = 12628

for i in range(articleAmount):

    # Creates the file name the scan will be saved as based on url given
    fileName = CreateFileName(url)
    
    # Gets raw iframe tag in order to etract the GetPDF request number
    raw_iframe = getsrc(url)

    # Creates the GetPdfFile used for digitalization
    GetPDFUrl = CreateGetPDf(raw_iframe)

    # Gets the https url to the next url
    nextArticle = getNextArticle(url)

    # Save PDF links to list
    digitalize_start = time.time()

    # Example data to add
    new_data = [
        {"url": GetPDFUrl, "name": fileName}
    ]

    # Check if file exists; if not, write header
    try:
        # If file doesn't exist, write the header first
        with open(csv_file, 'x', newline='') as csvfile:
            fieldnames = ['url', 'name']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
    except FileExistsError:
        pass  # File already exists; skip header writing

    append_to_csv(csv_file, new_data)
    print(f"page {fileName} succesfully stored in {csv_file}")

    elapsed_time = time.time() - start_time  # Calculate elapsed time
    # Convert to days, hours, minutes, and seconds
    days = int(elapsed_time // (24 * 3600))  # Total days
    elapsed_time %= (24 * 3600)  # Remaining seconds after removing days
    hours = int(elapsed_time // 3600)  # Total hours
    elapsed_time %= 3600  # Remaining seconds after removing hours
    minutes = int(elapsed_time // 60)  # Total minutes
    seconds = elapsed_time % 60  # Remaining seconds
    print(f"Execution time: {days} days, {hours} hours, {minutes} minutes, and {seconds:.2f} seconds")

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

print(f'Saved {articleAmount} GetPDFURls starting at article "the_lamoni_chronicle_usa_iowa_lamoni_19330921_english_1"')
print(f"Execution time: {days} days, {hours} hours, {minutes} minutes, and {seconds:.2f} seconds")