
### AOAI Document Indexer Demo

The AOAI Document Indexer is an automated solution tailored to download, process, and index an assortment of documents such as PDFs, Word documents (.docx), and PowerPoint files (.pptx) stored in an Azure Blob Storage account. It leverages Python to perform text extraction, text embeddings using Azure OpenAI, and employs Azure Cognitive Search alongside Azure Document Intelligence (formerly known as Form Recognizer) to efficiently index and make the documents searchable.

#### Usage Instructions

1.  Clone the repository to your local machine.
    
2.  Install Python 3.6 or higher.
    
3.  Navigate to the repository directory.
    
4.  Install the necessary package dependencies by executing:
    
    ```
    pip install -r requirements.txt
    ```
    
5.  Create a  `.env`  file with your Azure service credentials to set up the required environment variables.
    
6.  Ensure each document in the Azure Blob Storage has a corresponding  `.metadata.txt`  with at least two lines of metadata.
    
7.  Run the tool using the command:
    
    ```
    python test.py  
    ```
    

#### Metadata File Requirement

A crucial prerequisite for the indexing process is the presence of a  `.metadata.txt`  file alongside each document in the Blob Storage. The  `.metadata.txt`  file should contain at least two lines of text, where:

-   The first line is treated as the source URL of the document.
-   The second line is used for tagging purposes and can include descriptors or keywords that pertain to the document.

This metadata becomes part of the indexed information and is instrumental in enhancing the search functionality within Azure Cognitive Search.

#### Architecture Overview

```mermaid
flowchart TD
    A[Azure Blob Storage<br/>Contains Documents and metadata] -- Download --> B[AOAI Document Indexer]
    B -- Text & Metadata Extraction --> C[Azure Document Intelligence<br/>For PDF, DOCX, PPTX content]
    B -- Text Embeddings --> D[Azure OpenAI<br/>Generates text embeddings]
    B -- Indexing --> E[Azure Cognitive Search<br/>Document search and retrieval]

    subgraph Azure Cloud
    C
    D
    E
    end

    click A "https://portal.azure.com" "Azure Blob Storage"
    click C "https://portal.azure.com" "Azure Document Intelligence"
    click D "https://portal.azure.com" "Azure OpenAI"
    click E "https://portal.azure.com" "Azure Cognitive Search"
```

The diagram above depicts the flow of data and the integration of different Azure services within the AOAI Document Indexer system:

1.  Documents and their corresponding metadata files are stored in Azure Blob Storage.
2.  The AOAI Document Indexer downloads the documents and  `.metadata.txt`  files.
3.  Azure Document Intelligence is utilized for content extraction from documents.
4.  Azure OpenAI is used to generate text embeddings to enhance semantic search capabilities.
5.  Azure Cognitive Search is where all the indexed data is stored, allowing for efficient searching and retrieval.

### Process


```mermaid
flowchart TB
    start((Start)) --> A[Azure Blob Storage<br/>Download Documents and .metadata.txt files]
    A -->|Files Downloaded| B[Local Processing<br/>Use Azure Document Intelligence<br/>to extract text]
    B -->|Text Extracted| C[Azure OpenAI<br/>Generate text embeddings]
    C -->|Embeddings Created| D[Upload to Azure Cognitive Search<br/>Index text and embeddings]
    D -->|Data Indexed| End((End))

    style start fill:#bbf,stroke:#333,stroke-width:2px
    style End fill:#bbf,stroke:#333,stroke-width:2px
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style B fill:#f96,stroke:#333,stroke-width:2px
    style C fill:#9f9,stroke:#333,stroke-width:2px
    style D fill:#6bf,stroke:#333,stroke-width:2px
```

The diagram above illustrates the sequential order of operations executed by the AOAI Document Indexer:

1.  The process begins by downloading the necessary files, which include documentation and associated  `.metadata.txt`  files, from Azure Blob Storage.
    
2.  Local processing then takes place where Azure Document Intelligence is utilized to accurately extract text from downloaded documents.
    
3.  Upon successful text extraction, Azure OpenAI is engaged to generate the appropriate text embeddings (vectors), which facilitate advanced semantic search capabilities.
    
4.  Finally, both the extracted text and generated embeddings are uploaded and indexed within Azure Cognitive Search, creating a rich and searchable dataset that powers the AI search functionality.
    

This workflow ensures that each step is completed before moving on to the next, guaranteeing that the data is fully prepared and optimized for search before being made available in Azure Cognitive Search.


#### Azure AI Integration Detail

-   **Azure Cognitive Search:**  Offers advanced search capabilities, managing and querying the indexed data.
-   **Azure OpenAI:**  Enhances search by providing vector embeddings for semantic understanding, allowing users to search by meaning rather than specific keywords.
-   **Azure Document Intelligence:**  Extracts content from documents, converting them into structured data that can be indexed and searched.

#### Developer Notes

Developers must ensure the secure handling of Azure service credentials in  `.env`  files and comply with organizational security policies in production environments.

Adherence to the metadata file requirement is imperative for the proper functioning of the indexer, as it provides valuable context that enriches the search experience.

#### Maintainer’s Note:

The demonstration of the AOAI Document Indexer here is a simplified model for usage illustration purposes. It is strongly recommended to adopt security best practices for production deployments, including credential management, error handling strategies, and performance optimization to cater to your specific organizational needs and use cases.
