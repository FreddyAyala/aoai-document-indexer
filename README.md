
### AOAI Document Indexer Demo

The AOAI Document Indexer is an automated solution designed to download, process, and index PDF documents stored in an Azure Blob Storage account. This tool utilizes Python to handle the extraction of text from PDFs, generation of text embeddings using Azure OpenAI, and indexing the results in Azure Cognitive Search for efficient searching and retrieval.

### Usage Instructions

1.  Clone the repository to your local machine.
2.  Install Python 3.6 or higher.
3.  Navigate to the repository directory.
4.  Install the necessary package dependencies by executing:
    
    ```
    pip install -r requirements.txt
    
    ```
    
5.  Set up the required environment variables by creating a  `.env`  file with your Azure service credentials.
6.  Run the tool using the command:
    
    ```
    python test.py
    
    ```
    

### Functionality Overview

The tool operates by first downloading designated PDF files from Azure Blob Storage. It then processes the files, extracting text and handling metadata before generating embeddings for the text chunks. These embeddings are created using Azure OpenAI services. Finally, the tool indexes the text and embeddings to facilitate efficient and accurate searches within Azure Cognitive Search.

### Error Handling

The tool includes error handling to ensure smooth operation. In the event of an error, detailed logs are produced, and the document in question is recorded as failed, allowing for easy identification and troubleshooting.

### Main Components

-   `test.py`: The main script that calls other modules to perform the indexing tasks.
-   `processor.py`: Manages the processing of PDF files and keeps track of which files have been successfully processed or have failed.
-   `indexer.py`: Handles the creation of embeddings and indexing within Azure Cognitive Search.
-   `blob.py`: Downloads files from Azure Blob Storage.
-   `common.py`: Contains utility functions and classes for setting up and managing Azure Cognitive Search components.

### Additional Information

This tool is designed to work seamlessly with Azure services, leveraging advanced techniques and services to handle large volumes of textual data and provide an efficient search experience
