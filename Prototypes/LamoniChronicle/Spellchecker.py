import os
import language_tool_python

def spell_check_document(input_file, output_file):
    # Initialize LanguageTool
    tool = language_tool_python.LanguageTool('en-US')
    
    # Read the input file
    with open(input_file, "r", encoding="utf-8") as file:
        content = file.read()
    
    # Correct the content
    corrected_content = tool.correct(content)
    
    # Write the corrected content to the output file
    with open(output_file, "w", encoding="utf-8") as file:
        file.write(corrected_content)
    
    print(f"Spell check completed. Cleaned document saved as {output_file}.")

def process_multiple_files(input_dir, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Process all text files in the input directory
    for filename in os.listdir(input_dir):
        if filename.endswith(".txt"):  # Process only .txt files
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            print(f"Processing: {filename}")
            spell_check_document(input_path, output_path)

    print("All files processed successfully.")


input_directory = "CleanedMarkDown"
output_directory = "CleanedORC"

process_multiple_files(input_directory, output_directory)