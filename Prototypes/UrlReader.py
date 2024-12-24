import csv

# File name of the CSV file
csv_file = 'GetPDFUrls.csv'

# Open the CSV file for reading
with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
    # Create a DictReader object
    reader = csv.DictReader(csvfile)
    
    # Iterate over each row in the CSV
    for url,name in enumerate(reader):
        # Extract values into variables
        print(url, name)
