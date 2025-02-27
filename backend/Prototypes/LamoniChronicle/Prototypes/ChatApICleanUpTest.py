import os
import openai
from pathlib import Path
from Prototypes.ChatAPICleanUp import setup_openai_api, process_markdown_file
import tiktoken

def count_tokens(text, model="gpt-3.5-turbo"):
    """Count the number of tokens in a text string"""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

def test_markdown_cleanup():
    # Setup OpenAI API
    setup_openai_api()

    # Define input and output directories
    input_dir = Path("RegularORC")
    test_output_dir = Path("TestCleanedORC")

    # Create test output directory if it doesn't exist
    test_output_dir.mkdir(exist_ok=True)

    # Get first 5 markdown files
    markdown_files = list(input_dir.glob("*.md"))[:5]
    
    total_input_tokens = 0
    total_output_tokens = 0
    
    print("Starting test processing of first 5 files...")
    print("-" * 50)

    for markdown_file in markdown_files:
        print(f"\nProcessing: {markdown_file}")
        
        # Read original content and count tokens
        with open(markdown_file, 'r', encoding='utf-8') as file:
            original_content = file.read()
        input_tokens = count_tokens(original_content)
        total_input_tokens += input_tokens
        
        # Process the file
        cleaned_content = process_markdown_file(markdown_file)
        
        if cleaned_content:
            # Count output tokens
            output_tokens = count_tokens(cleaned_content)
            total_output_tokens += output_tokens
            
            # Save the cleaned content
            output_path = test_output_dir / markdown_file.name
            try:
                with open(output_path, 'w', encoding='utf-8') as file:
                    file.write(cleaned_content)
                
                # Print statistics for this file
                print(f"File: {markdown_file.name}")
                print(f"Input tokens: {input_tokens}")
                print(f"Output tokens: {output_tokens}")
                print(f"Successfully saved to: {output_path}")
                
            except Exception as e:
                print(f"Error saving {output_path}: {str(e)}")
        else:
            print(f"Error processing {markdown_file}")

    # Print summary statistics
    print("\n" + "=" * 50)
    print("SUMMARY")
    print("=" * 50)
    print(f"Total files processed: {len(markdown_files)}")
    print(f"Total input tokens: {total_input_tokens}")
    print(f"Total output tokens: {total_output_tokens}")
    print(f"Average tokens per file: {total_input_tokens / len(markdown_files):.2f} (input), "
          f"{total_output_tokens / len(markdown_files):.2f} (output)")
    
    # Estimate cost (using approximate pricing)
    input_cost = (total_input_tokens / 1000) * 0.01  # Adjust rate as needed
    output_cost = (total_output_tokens / 1000) * 0.03  # Adjust rate as needed
    total_cost = input_cost + output_cost
    
    print(f"\nEstimated cost: ${total_cost:.4f}")

if __name__ == "__main__":
    test_markdown_cleanup()
