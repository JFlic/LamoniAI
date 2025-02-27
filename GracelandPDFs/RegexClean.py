import os
import re

# Define input and output directories
input_directory = r"C:\Users\IT Lab VR\Desktop\LamoniAI\GracelandPDFs\TempDocumentStore"
output_directory = r"C:\Users\IT Lab VR\Desktop\LamoniAI\GracelandPDFs\CleanedMarkDown"

# Ensure output directory exists
os.makedirs(output_directory, exist_ok=True)

# Define regex cleaning rules
cleaning_patterns = [
    (r"\s{2,}", " "),  # Remove excessive spaces
    (r"(?<!\w)-\s+", ""),  # Fix hyphenated words that were split across lines
    (r"([a-z])\s+([A-Z])", r"\1. \2"),  # Add missing periods between sentences
    (r"\s*\\\s*", ""),  # Remove random backslashes
    (r"(\w)'(\s)", r"\1’\2"),  # Convert straight apostrophes to typographic ones
    (r"[•<>^*]", "") # Remove unwanted random characters like • < > ^
]

# Process all .md files
for filename in os.listdir(input_directory):
    if filename.endswith(".md"):
        input_file_path = os.path.join(input_directory, filename)
        output_file_path = os.path.join(output_directory, filename)

        with open(input_file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Apply regex transformations
        for pattern, replacement in cleaning_patterns:
            content = re.sub(pattern, replacement, content)

        # Save cleaned content in the new directory
        with open(output_file_path, "w", encoding="utf-8") as file:
            file.write(content)

print("All markdown files cleaned and saved to 'cleanedmarkdown' successfully!")
