import os
import re
from spellchecker import SpellChecker
import language_tool_python

# Directories
source_dir = "/Users/jackflickinger/Desktop/GracelandGPT/RawDigitalizedScans"
destination_dir = "/Users/jackflickinger/Desktop/GracelandGPT/SpellcheckedScans"

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
for filename in os.listdir(source_dir):
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


# # Directories
# source_dir = "/Users/jackflickinger/Desktop/GracelandGPT/RawDigitalizedScans"
# destination_dir = "/Users/jackflickinger/Desktop/GracelandGPT/SpellcheckedScans"

# # Create destination directory if it doesn't exist
# os.makedirs(destination_dir, exist_ok=True)

# # Initialize the spell checker
# spell = SpellChecker()

# # Function to check and fix spelling
# def correct_spelling(text):
#     words = text.split()
#     corrected_words = []
#     for word in words:
#         # Remove punctuation for spell checking
#         stripped_word = re.sub(r'[^\w\s]', '', word)
#         corrected_word = spell.correction(stripped_word)
#         # Preserve original word's punctuation
#         corrected_words.append(word.replace(stripped_word, corrected_word))
#     return " ".join(corrected_words)

# # Function to check and fix punctuation (basic example)
# def correct_punctuation(text):
#     # Add missing space after periods, commas, etc.
#     text = re.sub(r'([.,!?])([^\s])', r'\1 \2', text)
#     return text

# # Process each Markdown file
# for filename in os.listdir(source_dir):
#     if filename.endswith(".md"):
#         source_path = os.path.join(source_dir, filename)
#         destination_path = os.path.join(destination_dir, filename)

#         # Read the content of the file
#         with open(source_path, "r", encoding="utf-8") as file:
#             content = file.read()

#         # Correct spelling and punctuation
#         corrected_content = correct_spelling(content)
#         corrected_content = correct_punctuation(corrected_content)

#         # Save the corrected content
#         with open(destination_path, "w", encoding="utf-8") as file:
#             file.write(corrected_content)

# print(f"Spell check and punctuation correction completed. Files saved to {destination_dir}.")
