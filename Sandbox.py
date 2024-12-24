from symspellpy import SymSpell, Verbosity
import os

# Initialize SymSpell
max_edit_distance_dictionary = 2  # Maximum edit distance for word corrections
prefix_length = 7  # Length of prefixes for dictionary keys
sym_spell = SymSpell(max_edit_distance_dictionary, prefix_length)

# Load a frequency dictionary
# Download frequency_dictionary_en_82_765.txt from https://github.com/mammothb/symspellpy
dictionary_path = "frequency_dictionary_en_82_765.md"
sym_spell.load_dictionary(dictionary_path, term_index=0, count_index=1)

# Paths
input_dir = "/Users/jackflickinger/Desktop/GracelandGPT/RawDigitalizedScans"
output_dir = "/Users/jackflickinger/Desktop/GracelandGPT/SpellcheckedScans"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to correct text
def correct_text(text):
    # Lookup suggestions for misspelled words in a sentence
    corrected = sym_spell.lookup_compound(text, max_edit_distance_dictionary)
    return corrected[0].term if corrected else text

# Process each file
for file_name in os.listdir(input_dir):
    if file_name.endswith('.md'):  # Process only text files
        file_path = os.path.join(input_dir, file_name)
        
        with open(file_path, 'r') as file:
            text = file.read()
        
        # Correct text
        corrected_text = correct_text(text)
        
        # Save corrected text
        corrected_path = os.path.join(output_dir, file_name)
        with open(corrected_path, 'w') as corrected_file:
            corrected_file.write(corrected_text)

print("Spell check and corrections completed!")
