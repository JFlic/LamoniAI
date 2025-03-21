import os
import csv

# Folder containing the documents
doc_folder = "Horizons"

# Output CSV file
output_csv = "GetUrls.csv"

# File extensions to include
file_extensions = [".pdf", ".docx", ".md"]

base_url = "https://www.graceland.edu/alumni/horizons/"

# Read existing entries to avoid duplicates
existing_entries = set()
if os.path.exists(output_csv):
    with open(output_csv, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header row
        for row in reader:
            if len(row) >= 2:  # Ensure it's a valid row
                existing_entries.add(row[1])  # Add existing file names

# Get a list of all matching files in the folder
doc_files = [f for f in os.listdir(doc_folder) if any(f.endswith(ext) for ext in file_extensions)]

# Open CSV in append mode
with open(output_csv, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Write header if file is empty
    if os.stat(output_csv).st_size == 0:
        writer.writerow(["Link", "File Name"])

    # Append only new files
    for doc in doc_files:
        if doc not in existing_entries:  # Avoid duplicates
            doc_link = base_url
            writer.writerow([doc_link, doc])

print(f"CSV file '{output_csv}' has been updated with new document links and names.")
