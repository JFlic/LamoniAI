import os
import re
from spellchecker import SpellChecker
import language_tool_python
from tqdm.auto import tqdm

# Directories
source_dir = "/Users/jackflickinger/Desktop/LamoniAI/RegularORC"
destination_dir = "/Users/jackflickinger/Desktop/LamoniAI/SpellcheckedScans"

# Create destination directory if it doesn't exist
os.makedirs(destination_dir, exist_ok=True)

# Initialize LanguageTool
tool = language_tool_python.LanguageTool('en-US')

# Function to process a single Markdown file
def process_markdown_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()  # Read the entire file as a string
    corrected_content = tool.correct(content)  # Use LanguageTool for corrections
    return corrected_content

# Process all Markdown files in the source directory
for filename in tqdm(os.listdir(source_dir)):
    if filename.endswith(".md"):
        source_path = os.path.join(source_dir, filename)
        destination_path = os.path.join(destination_dir, filename)

        print(f"Processing: {filename}")

        # Correct the content of the file
        corrected_content = process_markdown_file(source_path)

        # Save the corrected content to the destination directory
        with open(destination_path, "w", encoding="utf-8") as file:
            file.write(corrected_content)

print(f"Spell check and grammar correction completed. Files saved to {destination_dir}.")