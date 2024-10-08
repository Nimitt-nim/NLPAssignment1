import os
import csv

def count_string_in_file(file_path, search_string):
    """Counts occurrences of a given string in a text file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            count = content.count(search_string)
        return count
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return 0

def generate_csv_file(folder_path, search_string, output_csv_file):
    """Extracts filenames and counts occurrences of a string, then creates a CSV file."""
    results = []
    
    # Loop through all files in the specified folder
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            count = count_string_in_file(file_path, search_string)
            results.append((filename, count))
    
    # Write the results to a CSV file
    with open(output_csv_file, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(['Source', 'Number of articles'])  # Header
        csv_writer.writerows(results)

# Specify your folder path and output file name
folder_path = '/Users/nimitt/Documents/NLP_new/NGramsDeduplicated1'  
output_csv_file = 'sources.csv'
search_string = '------------------------'

# Call the function to generate the CSV file
generate_csv_file(folder_path, search_string, output_csv_file)
