import requests
from requests.sessions import Session
from urllib.parse import urljoin

def list_files(site_url, folder_url, cookies):
    # Combine the site URL and the server-relative URL of the folder
    full_folder_url = urljoin(site_url, f"_api/web/GetFolderByServerRelativeUrl('{folder_url}')/Files")
    
    # Create a new session object
    session = Session()
    session.headers.update({'Accept': 'application/json;odata=verbose'})
    
    # Attach the cookies to the session
    session.cookies.update(cookies)
    
    # Make the request to list files
    response = session.get(full_folder_url)
    
    # Raise an exception if the call failed
    response.raise_for_status()
    
    # Process the JSON response
    files_data = response.json()['d']['results']
    file_list = [file['Name'] for file in files_data]
    return file_list

# Replace with your actual SharePoint site URL
site_url =  'https://microsofteur.sharepoint.com/teams/TestSharepointOnlineOAI/'

# Replace with your actual folder server-relative URL
folder_relative_url = '/Shared Documents/HR/'

# Replace with your actual cookies obtained from the browser
cookies = {
    'rtFa': ''
    'FedAuth': ''
}

# List all files in the SharePoint folder
files = list_files(site_url, folder_relative_url, cookies)
print(files)
