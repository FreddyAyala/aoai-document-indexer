
from lib.blob import download_blobs
#from lib.indexer import process_pdf
import os
from json import dumps
import logging
import traceback
from lib.log import log_info

from lib.processor import process_files
from dotenv import load_dotenv


try:
    # Set up logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    load_dotenv() 
    # Connection string to your storage account
    local_directory_name="data"
    local_directory = os.path.join(local_directory_name)
    log_info(f"Downloading Files")
    download_blobs(local_directory_name)
   
     
    log_info(f"Processing Files")
    process_files(local_directory)
    
     
except Exception as e:
    logging.error(f"{'-' * 50}")
    logging.error(f"An error occurred: {str(e)}")
    traceback = e.__traceback__
    while traceback:
        print("{}: {}".format(traceback.tb_frame.f_code.co_filename,traceback.tb_lineno))
        traceback = traceback.tb_next
    logging.error(f"{'-' * 50}")
