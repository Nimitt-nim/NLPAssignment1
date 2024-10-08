import hashlib
import os

# Function to generate a hash for a given text
def generate_hash(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()

# Deduplicate articles in multiple text files and save each file with the same name
def deduplicate_across_files(input_folder, output_folder, separator='------------------------'):
    seen_hashes = set()

    # Loop through all files in the input folder
    for filename in os.listdir(input_folder):
        file_path = os.path.join(input_folder, filename)

        # Ensure it's a text file (optional check)
        if os.path.isfile(file_path) and filename.endswith('.txt'):
            unique_articles = []
            # Read the file content
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Split content into articles using the separator
            articles = content.split(separator)
            print(articles)
            # Deduplicate the articles
            for article in articles:
                article = article.strip()  # Clean up whitespace
                if article:  # Ensure article is not empty
                    text_hash = generate_hash(article)

                    # If the hash is not in seen_hashes, add it to unique_articles
                    if text_hash not in seen_hashes:
                        seen_hashes.add(text_hash)
                        unique_articles.append(article)

            # Define output file path (same name as input but in output folder)
            output_path = os.path.join(output_folder, filename)

            # Write the unique articles back to the output file
            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write(f"\n{separator}\n".join(unique_articles))
                output_file.write(f"\n{separator}\n")  # End with a separator for consistency

# Specify the input folder and output folder
input_folder = 'NGramsCleanedData'  # Replace with your input folder path
output_folder = 'NGramsDeduplicatedData'  # Replace with your output folder path

# Ensure the output folder exists, if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Call the function
deduplicate_across_files(input_folder, output_folder)

print("Deduplication across files complete!")

