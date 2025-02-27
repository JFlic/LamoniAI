import os
import re
from tqdm.auto import tqdm

def clean_markdown(text: str) -> str:
    """
    Clean markdown formatting from text
    """
    # Remove markdown headers (##)
    text = re.sub(r'#+\s*', '', text)
    
    # Remove HTML comments and image tags
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    text = re.sub(r'<.*?>', '', text)
    
    # Remove markdown formatting characters
    text = text.replace('*', '')
    text = text.replace('_', '')
    text = text.replace('`', '')
    text = text.replace('|', '')
    text = text.replace('~', '')
    text = text.replace('{', '')
    text = text.replace('}', '')
    text = text.replace('[', '')
    text = text.replace(']', '')
    text = text.replace('\\', '')
    text = text.replace('°', '')
    text = text.replace('+', '')

    
    # Remove multiple spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
    return text

def process_markdown_files():
    count = 0
    # Create output directory if it doesn't exist
    output_dir = "CleanedMarkDown"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Input directory containing markdown files
    input_dir = r"C:\Users\IT Lab VR\Desktop\LamoniAI\LamoniChronicle\RegularORC"
    
    # Get list of markdown files
    md_files = [f for f in os.listdir(input_dir) if f.endswith('.md')]
    
    print(f"Found {len(md_files)} markdown files to process")
    
    # Process each file
    for md_file in tqdm(md_files, desc="Processing files"):
        if count == 10:
            break
        # Read markdown file
        with open(os.path.join(input_dir, md_file), 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Clean the content
        cleaned_content = clean_markdown(content)
        
        # Create output filename (change extension to .txt)
        output_filename = os.path.splitext(md_file)[0] + '.txt'
        
        # Write cleaned content to new file
        with open(os.path.join(output_dir, output_filename), 'w', encoding='utf-8') as f:
            f.write(cleaned_content)
        
        count += 1

# Run the processing
for i in range(10):
    process_markdown_files()

# Verify results
output_dir = "CleanedMarkDown"
cleaned_files = os.listdir(output_dir)
print(f"\nCreated {len(cleaned_files)} cleaned text files")

# Preview first few lines of first cleaned file
if cleaned_files:
    first_file = cleaned_files[0]
    print(f"\nPreview of {first_file}:")
    with open(os.path.join(output_dir, first_file), 'r', encoding='utf-8') as f:
        preview = f.read(500)
    print(preview + "...")