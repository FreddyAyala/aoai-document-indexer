import datetime
import hashlib
from json import dumps
import logging
import os
import traceback
from lib.data_preparation import create_or_update_search_index, upload_documents_to_index
from lib.data_utils import process_file
import pathlib

from azure.search.documents import SearchClient
#from lib.indexer import process_pdf

from lib.log import log_info

def process_files(local_directory):
    total_files_processed = 0
    # Calculate total time elapsed
    start_time = datetime.datetime.now()
    # Loop to process downloaded PDF files
    files = os.listdir(local_directory)
    print(files[0])
    for file in files:
        file_extension = pathlib.Path(file).suffix
        if file.endswith(".pdf") or file.endswith(".pptx") or file.endswith(".docx"):
            if file.endswith(".pptx") :
                print("toasty!")
            # Create a local file path for the downloaded file
            local_file_path = os.path.join(local_directory, file)

            # Log the processing file path
            log_info(f"Starting processing file: {file}")
            # Read metadata from metadata.txt file
            metadata_file_path = os.path.join(local_directory, f"{os.path.splitext(file)[0]}{file_extension}.metadata.txt")
            print(metadata_file_path)
            if os.path.exists(metadata_file_path):
                with open(metadata_file_path, 'r') as metadata_file:
                    metadata_lines = metadata_file.readlines()
                    metadata = [line.strip() for line in metadata_lines]
                log_info(f"Process file with metadata: {file} {metadata}")
                # Send metadata to the processing function
                print(local_file_path)
                if is_file_processed(file):
                    log_info(f"File already processed: {file}")
                    continue
                try:
                    #process_pdf(local_file_path, dumps(metadata))
                    result = process_file(file, os.path.join(local_directory),add_embeddings=True)
                    print("Creating index...")
                    my_index_name = os.environ["AZURE_SEARCH_INDEX"]
                    create_or_update_search_index(
                        service_name=os.environ["AZURE_SEARCH_SERVICE_NAME"],
                        index_name=my_index_name,
                        vector_config_name="default",
                        admin_key=os.environ["AZURE_SEARCH_ADMIN_KEY"],
                    )                  
                  
                    source_url = metadata[0] if metadata and len(metadata) > 0 else ""
                    tags = metadata[1] if metadata and len(metadata) > 1 else ""

                    upload_documents_to_index(
                        service_name=os.environ["AZURE_SEARCH_SERVICE_NAME"],
                        index_name=my_index_name,
                        docs=result[0].chunks,
                        admin_key=os.environ["AZURE_SEARCH_ADMIN_KEY"],
                        sourceurl=source_url,
                        tags=tags
                    )
                    print(f"Index {my_index_name} created.")
                    
                    
                    log_info(f"Processing file finished: {file}")
                    total_files_processed = total_files_processed + 1
                    # Write processed file information to processed.txt
                    processed_info = f"{file}|{hash_file(local_file_path)}|{get_current_date()}\n"
                    write_to_processed_file(processed_info)
                    
                except Exception as e:
                    logging.error(f"An error occurred while processing file: {file}")
                    logging.error(f"Error message: {str(e)}")
                    traceback.print_exc()
                     # Write failed file information to failed.txt
                    failed_info = f"{file}|{str(e)}|{get_current_date()}\n"
                    write_to_failed_file(failed_info)


    
    end_time = datetime.datetime.now()
    total_time_elapsed = end_time - start_time

    print(f"Total files processed: {total_files_processed}")
    print(f"Total time elapsed: {total_time_elapsed}")

def hash_file(file_path):
    # Calculate the hash of the file content
    with open(file_path, 'rb') as file:
        content = file.read()
        file_hash = hashlib.sha256(content).hexdigest()
    return file_hash

def get_current_date():
    # Get the current date in the desired format
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    return current_date

def write_to_processed_file(processed_info):
    # Write processed file information to processed.txt
    with open("processed.txt", 'a') as processed_file:
        processed_file.write(processed_info)
        
def is_file_processed(file_name):
    # Check if the file has already been processed
    with open("processed.txt", 'r') as processed_file:
        processed_lines = processed_file.readlines()
        processed_files = [line.split("|")[0] for line in processed_lines]
    return file_name in processed_files
def write_to_failed_file(failed_info):
    # Write failed file information to failed.txt
    with open("failed.txt", 'a') as failed_file:
        failed_file.write(failed_info)