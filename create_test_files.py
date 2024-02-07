import os
import shutil
import random
import string

# Define the source and destination folders
source_folder = 'data'
destination_folder = 'output'

# Get a list of all files in the source folder
files = os.listdir(source_folder)

# Iterate over each file in the source folder
for file in files:
    # Check if the file has the .pdf extension
    if file.endswith('.pdf'):
        # Get the common name by removing the extension
        common_name = os.path.splitext(file)[0]
        
        # Generate 100 random names
        random_names = [''.join(random.choices(string.ascii_lowercase, k=10)) for _ in range(100)]
        
        # Iterate over each random name
        for random_name in random_names:
            # Create the new file names
            new_pdf_file = f'{common_name}_{random_name}.pdf'
            new_metadata_file = f'{common_name}_{random_name}.pdf.metadata.txt'
            
            # Copy the original .pdf file and preserve the content
            shutil.copy2(os.path.join(source_folder, file), os.path.join(destination_folder, new_pdf_file))
            
            # Copy the original .metadata.txt file and preserve the content
            shutil.copy2(os.path.join(source_folder, f'{common_name}.pdf.metadata.txt'), os.path.join(destination_folder, new_metadata_file))
