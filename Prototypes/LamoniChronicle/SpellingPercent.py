import os
from symspellpy import SymSpell, Verbosity
from tqdm import tqdm

# Load SymSpell dictionary
sym_spell = SymSpell(max_dictionary_edit_distance=4)
dictionary_path = "frequency_dictionary_en_82_765.txt"

if not sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1):
    print("Error: Dictionary file not found or failed to load!")
else:
    print(f"Dictionary loaded! Words count: {len(sym_spell.words)}")

# Parameters
INPUT_DIR = "CleanedMarkDown"
OUTPUT_DIR = "ReadyForRAG"
SPELLING_THRESHOLD = 20  # Minimum percentage of correct words for RAG usability

os.makedirs(OUTPUT_DIR, exist_ok=True)


def analyze_text(file_path):
    """ Reads a text file, checks spelling, and calculates error percentage. """
    with open(file_path, "r", encoding="utf-8") as file:
        words = file.read().split()

    total_words = len(words)
    if total_words == 0:
        return 100, 0  # Empty files are considered "clean"

    # Count misspelled words
    misspelled_count = sum(
        1 for word in words if not sym_spell.lookup(word, Verbosity.CLOSEST, max_edit_distance=4)
    )
    print(total_words)
    print(misspelled_count)

    error_percentage = (misspelled_count / total_words) * 100
    accuracy_percentage = 100 - error_percentage

    return accuracy_percentage, misspelled_count

def process_documents(input_dir, output_dir):
    """ Process all text files and generate reports. """
    report_lines = []
    
    for filename in tqdm(os.listdir(input_dir), desc="Processing Files"):
        if filename.endswith(".txt"):
            file_path = os.path.join(input_dir, filename)
            accuracy, misspelled_count = analyze_text(file_path)
            
            # Determine if file is usable for RAG
            is_usable = accuracy >= SPELLING_THRESHOLD
            status = "✅ Suitable for RAG" if is_usable else "❌ Needs Cleaning"

            # Save report
            report_line = f"{INPUT_DIR}\{filename}: Accuracy {accuracy:.2f}% | Misspelled: {misspelled_count} | {status}"
            report_lines.append(report_line)
    
    # Save summary report
    report_path = os.path.join(output_dir, "spelling_analysis_report.txt")
    with open(report_path, "w", encoding="utf-8") as report_file:
        report_file.write("\n".join(report_lines))

    print(f"\n📄 Spelling analysis completed! Report saved at: {report_path}")

# Run the pipeline
process_documents(INPUT_DIR, OUTPUT_DIR)
