import os
from simhash import Simhash

# Function to deduplicate articles in multiple text files using Simhash
def deduplicate_using_simhash(input_folder, output_folder, separator='------------------------', threshold=3):
    seen_hashes = set()
    article_count = 0
    unique_count = 0

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
            articles = [article.strip() for article in articles if article.strip()]

            # Deduplicate the articles
            for article in articles:
                article_hash = Simhash(article)
                article_count += 1
                is_duplicate = False

                # Check against already seen hashes
                for seen_hash in seen_hashes:
                    if article_hash.distance(Simhash(seen_hash)) <= threshold:
                        is_duplicate = True
                        break

                if not is_duplicate:
                    seen_hashes.add(article_hash.value)  # Store the integer value of Simhash
                    unique_articles.append(article)
                    unique_count += 1

            # Define output file path (same name as input but in output folder)
            output_path = os.path.join(output_folder, filename)

            # Write the unique articles back to the output file
            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write(f"\n{separator}\n".join(unique_articles))
                output_file.write(f"\n{separator}\n")  # End with a separator for consistency

    print(f"Processed {article_count} articles. Found {unique_count} unique articles.")

# Specify the input folder and output folder
input_folder = 'NGramsDeduplicated1'  # Replace with your input folder path
output_folder = 'NGramsDeduplicated2'  # Replace with your output folder path

# Ensure the output folder exists, if not, create it
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Call the function
deduplicate_using_simhash(input_folder, output_folder)

print("Deduplication using Simhash complete!")
