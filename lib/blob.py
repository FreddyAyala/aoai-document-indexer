from dotenv import load_dotenv
from lib.indexer import process_pdf
import os
from azure.storage.blob import BlobServiceClient
from json import dumps
import logging

def download_blobs(directory):
    try:
        # Set up logging
        #logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        # Pull documents from a storage account
        load_dotenv() 
        # Connection string to your storage account
        connection_string = os.environ["AZURE_BLOB_CONNECTION_STRING"]

        # Name of the container in your storage account
        container_name = "data"

        # Local directory to save the downloaded files
        local_directory = os.path.join(directory)

        # Create a BlobServiceClient object
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)

        # Get a reference to the container
        container_client = blob_service_client.get_container_client(container_name)

        # List all blobs in the container
        blobs = container_client.list_blobs()

        # Loop to download PDF files or metadata.txt files
        for blob in blobs:
            if blob.name.endswith(".pdf") or blob.name.endswith(".metadata.txt"):
                try:
                    # Create a local file path for the downloaded file
                    local_file_path = os.path.join(local_directory, blob.name)

                    # Check if the file already exists and its size is greater than zero
                    if os.path.exists(local_file_path) and os.path.getsize(local_file_path) > 0:
                        print(f"File already exists: {local_file_path}")
                        continue

                    # Download the blob to the local file
                    with open(local_file_path, "wb") as file:
                        blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob.name)
                        file.write(blob_client.download_blob().readall())

                    # Log the downloaded file path
                    logging.info(f"{'-' * 50}")
                    logging.info(f"Downloaded file: {local_file_path}")
                    logging.info(f"{'-' * 50}")

                except Exception as e:
                    # Log the error and continue to the next blob
                    logging.error(f"{'-' * 50}")
                    logging.error(f"Error downloading blob: {blob.name}. Error: {str(e)}")
                    logging.error(f"{'-' * 50}")
                    continue

    except Exception as e:
        logging.error(f"{'-' * 50}")
        logging.error(f"An error occurred: {str(e)}")
        logging.error(f"{'-' * 50}")