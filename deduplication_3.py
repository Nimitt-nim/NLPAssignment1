import os
from datasketch import MinHash, MinHashLSH
import hashlib

def minhash_signature(article, num_perm=128):
    """Generate a MinHash signature for an article."""
    m = MinHash(num_perm=num_perm)
    for word in article.split():
        m.update(word.encode('utf8'))
    return m

def deduplicate_using_minhash(input_folder, output_folder, separator='------------------------', similarity_threshold=0.95):
    unique_articles_by_file = {}

    filenames = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
    
    for filename in filenames:
        file_path = os.path.join(input_folder, filename)
        
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            
            articles = content.split(separator)
            articles = [article.strip() for article in articles if article.strip()]
            
            if articles:
                lsh = MinHashLSH(threshold=similarity_threshold, num_perm=128)
                seen_articles = {}

                for i, article in enumerate(articles):
                    sig = minhash_signature(article)
                    # Check for similar articles
                    similar = lsh.query(sig)
                    
                    if not similar:  # No similar articles found
                        lsh.insert(f'article_{i}', sig)  # Insert with a unique key
                        unique_articles_by_file.setdefault(filename, []).append(article)
                        seen_articles[f'article_{i}'] = article  # Track seen articles
                
            
            # Ensure unique articles are saved back
            if filename not in unique_articles_by_file:
                unique_articles_by_file[filename] = []

            output_path = os.path.join(output_folder, filename)
            with open(output_path, 'w', encoding='utf-8') as output_file:
                output_file.write(f"\n{separator}\n".join(unique_articles_by_file[filename]))
                output_file.write(f"\n{separator}\n")

# Specify folders
input_folder = 'NGramsDeduplicated1'  # Replace with your input folder path
output_folder = 'NGramsDeduplicated2'  # Replace with your output folder path


# Ensure output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Call the deduplication function
deduplicate_using_minhash(input_folder, output_folder)

print("MinHash Deduplication complete!")
