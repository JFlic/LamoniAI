import os
import openai
from pathlib import Path
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Load environment variables from .env file
load_dotenv()

def setup_openai_api():
    """Setup OpenAI API with key from environment variable"""
    openai.api_key = os.getenv('OPENAI_API_KEY')
    if not openai.api_key:
        raise ValueError("Please set the OPENAI_API_KEY environment variable")

def process_markdown_file(input_path):
    """Process a single markdown file using Deepseek"""
    try:
        model_name = "deepseek-ai/deepseek-coder-6.7b-instruct"
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)
        
        with open(input_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        prompt = f"### Instruction: Clean up this markdown by fixing formatting and spelling issues while preserving the original content:\n\n{content}\n\n### Response:"
        inputs = tokenizer(prompt, return_tensors="pt")
        outputs = model.generate(**inputs, max_length=len(content) + 100)
        cleaned_content = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        return cleaned_content
    except Exception as e:
        print(f"Error processing {input_path}: {str(e)}")
        return None

def main():
    # Setup OpenAI API
    setup_openai_api()

    # Define input and output directories
    input_dir = Path("RegularORC")
    output_dir = Path("CleanedORC")

    # Create output directory if it doesn't exist
    output_dir.mkdir(exist_ok=True)

    # Process all markdown files
    for markdown_file in input_dir.glob("*.md"):
        print(f"Processing: {markdown_file}")
        
        # Generate output path
        output_path = output_dir / markdown_file.name
        
        # Process the file
        cleaned_content = process_markdown_file(markdown_file)
        
        if cleaned_content:
            # Save the cleaned content
            try:
                with open(output_path, 'w', encoding='utf-8') as file:
                    file.write(cleaned_content)
                print(f"Successfully processed and saved: {output_path}")
            except Exception as e:
                print(f"Error saving {output_path}: {str(e)}")
        else:
            print(f"Skipping {markdown_file} due to processing error")

if __name__ == "__main__":
    main()
