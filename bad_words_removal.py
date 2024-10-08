import os
import re
import pandas as pd

# Global variables for words
porn_words = []
bad_bengali_words = []

# Function to load words from a CSV file into a global list
def load_words_from_csv(file_path, word_list):
    df = pd.read_csv(file_path)
    word_list.extend(df.iloc[:, 0].tolist())  # Assuming words are in the first column

# Function to check if the filename has any pornographic English words
def check_filename_for_porn(filename):
    for word in porn_words:
        if word.lower() in filename.lower():
            return True
    return False

# Function to remove English characters from text
def remove_english_characters(text):
    return re.sub(r'[a-zA-Z]', '', text)

# Function to remove bad Bengali words
def remove_bad_bengali_words(text):
    for word in bad_bengali_words:
        text = text.replace(word, '')
    return text

# Main function to process a single file
def process_file(input_filename, output_filename):
    # Check if filename contains any pornographic words
    if check_filename_for_porn(input_filename):
        print(f"Filename '{input_filename}' contains inappropriate words. Exiting.")
        return

    # Read the file
    with open(input_filename, 'r', encoding='utf-8') as file:
        content = file.read()

    # Remove English characters
    content = remove_english_characters(content)

    # Remove bad Bengali words
    content = remove_bad_bengali_words(content)

    # Write the cleaned content to a new file
    with open(output_filename, 'w', encoding='utf-8') as output_file:
        output_file.write(content)

# Function to load words and process files in a folder
def process_files_in_folder(input_folder, output_folder, porn_words_file, bad_bengali_words_file):
    # Load the lists of words
    load_words_from_csv(porn_words_file, porn_words)
    load_words_from_csv(bad_bengali_words_file, bad_bengali_words)

    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Process each file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):  # Process only text files
            input_file_path = os.path.join(input_folder, filename)
            output_file_path = os.path.join(output_folder, filename)
            process_file(input_file_path, output_file_path)

# Example usage
input_folder = "NGramsSortedData"  # Replace with your input folder path
output_folder = "NGramsCleanedData"  # Output folder name
porn_words_file = "porn_words_english.csv"  # Replace with your porn words CSV file path
bad_bengali_words_file = "bad_words_bengali.csv"  # Replace with your bad Bengali words CSV file path

process_files_in_folder(input_folder, output_folder, porn_words_file, bad_bengali_words_file)