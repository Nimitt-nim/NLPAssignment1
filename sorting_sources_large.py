import re
import os

# Directory to store the output files
output_dir = 'NGramsSortedData'
os.makedirs(output_dir, exist_ok=True)  # Create the directory if it doesn't exist


raw_data_dir = 'NGramsData'
raw_files = [f for f in os.listdir(raw_data_dir) if f.endswith('.raw')]
for raw_name in raw_files:
    # Open the input file in read mode
    with open(f"{raw_data_dir}/{raw_name}", 'r', encoding='utf-8', errors='replace') as infile:
        uri = 'https://0init/'  # Placeholder URI to start
        lines_to_write = []
        
        # Read the input file line by line
        for line in infile:
            if "uri:" in line:
                # If we encounter a new URI, write the collected data to a domain-specific file
                if uri and lines_to_write:
                    # Extract the domain from the URI
                    domain_match = re.search(r'//([^/]+)/', uri)
                    if domain_match:
                        domain = domain_match.group(1)  # Extract the domain name
                        
                        # Replace invalid characters in the domain to make it a valid filename
                        filename = re.sub(r'[^\w]', '_', domain) + '.txt'
                        
                        # Write the data to a domain-specific file
                        with open(os.path.join(output_dir, filename), 'a', encoding='utf-8') as outfile:
                            outfile.write("\n------------------------\n")
                            outfile.writelines(lines_to_write)
                            outfile.write("------------------------\n")

                # Extract the new URI from the current line
                uri_match = re.search(r'uri:(http[^\s]+)', line)
                if uri_match:
                    uri = uri_match.group(1)  # Extract the full URI
                
                # Reset the buffer for the next URI
                lines_to_write = []
            
            # Collect other data related to the URI
            else:
                lines_to_write.append(line)
        
        # Write the last URI and its corresponding data (if any)
        if uri and lines_to_write:
            domain_match = re.search(r'//([^/]+)/', uri)
            if domain_match:
                domain = domain_match.group(1)
                filename = re.sub(r'[^\w]', '_', domain) + '.txt'
                
                with open(os.path.join(output_dir, filename), 'a', encoding='utf-8') as outfile:
                    outfile.write("\n------------------------\n")
                    outfile.writelines(lines_to_write)
                    outfile.write("------------------------\n")

    print(f"Processing complete for raw{raw_name}")