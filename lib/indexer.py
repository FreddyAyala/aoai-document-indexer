import base64
import hashlib
from urllib.parse import quote
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
import os
from openai import AzureOpenAI
from azure.identity import get_bearer_token_provider
from azure.search.documents.indexes import SearchIndexClient
from lib.common import create_search_index
from langchain_community.document_loaders import PyPDFLoader
from lib.common import plot_chunk_histogram, get_token_length
from langchain.text_splitter import RecursiveCharacterTextSplitter
from lib.common import get_encoding_name
from json import dumps

from lib.data_utils import process_file

def process_pdf(filename, metadata):
    load_dotenv() # take environment variables from .env.

    # Variables not used here do not need to be updated in your .env file
    search_endpoint = os.environ["AZURE_SEARCH_SERVICE_ENDPOINT"]
    azure_openai_endpoint = os.environ["AZURE_OPENAI_ENDPOINT"]
    azure_openai_embedding_deployment_id = os.environ["AZURE_OPENAI_EMBEDDING_DEPLOYMENT_ID"]
    recursivetextsplitter_searchindex = os.environ["AZURE_SEARCH_LANGCHAIN_RECURSIVETEXTSPLITTER_INDEX"]

    search_credential = AzureKeyCredential(os.environ["AZURE_SEARCH_ADMIN_KEY"]) if len(os.environ["AZURE_SEARCH_ADMIN_KEY"]) > 0 else DefaultAzureCredential()
    azure_openai_key = os.environ["AZURE_OPENAI_KEY"] if len(os.environ["AZURE_OPENAI_KEY"]) > 0 else None

    azure_openai_client = None
    if azure_openai_key:
        azure_openai_client = AzureOpenAI(
            api_key=azure_openai_key, 
            api_version="2023-05-15",
            azure_deployment=azure_openai_embedding_deployment_id,
            azure_endpoint=azure_openai_endpoint)
    else:
        azure_openai_client = AzureOpenAI(
            azure_ad_token_provider=get_bearer_token_provider(DefaultAzureCredential(), "https://cognitiveservices.azure.com/.default"),
            api_version="2023-05-15",
            azure_deployment=azure_openai_embedding_deployment_id,
            azure_endpoint=azure_openai_endpoint)

    search_index_client = SearchIndexClient(endpoint=search_endpoint, credential=search_credential)
    rts_searchindex = create_search_index(
        recursivetextsplitter_searchindex,
        azure_openai_endpoint,
        azure_openai_embedding_deployment_id,   
        azure_openai_key
    )
    search_index_client.create_or_update_index(rts_searchindex)

  

    recursive_search_client = search_index_client.get_search_client(recursivetextsplitter_searchindex)

    filename_without_extension = os.path.basename(filename).replace(".", "_")
    filename_hash = hashlib.sha256(filename_without_extension.encode()).hexdigest()
    process_file()
    
    docs = [
        {
            "parent_id": "0",
            "chunk_id": f"{filename_hash}_0_0_{i}",
            "chunk": chunk.page_content,
            "title": filename,
            "vector": recursive_text_splitter_embeddings[i],
            "metadata": metadata
        }
        for i, chunk in enumerate(recursive_text_splitter_chunks)
    ]
    

    recursive_search_client.upload_documents(docs)
    print("Uploaded chunks and embeddings for recursive text splitter")


