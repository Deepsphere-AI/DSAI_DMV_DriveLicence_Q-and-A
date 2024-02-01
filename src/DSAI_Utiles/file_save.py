import os

import os
from PyPDF2 import PdfReader

def save_uploaded_file(file):
    """
    Saves an uploaded file to the 'Result' directory and counts the number of pages if it is a PDF.

    Parameters:
    file (UploadedFile): The file object to save. Expected to have 'name' and 'getbuffer()' attributes.

    Returns:
    tuple: A tuple containing the file path and the number of pages in the PDF, or None if an error occurs.
    """
    # Set the directory where the file will be saved
    directory = "Result"
    
    # Create the Result directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Set the file path
    file_path = os.path.join(directory, file.name)

    # Write the file to the specified directory
    try:
        with open(file_path, "wb") as f:
            f.write(file.getbuffer())
    except Exception as e:
        print(f"Error writing file: {e}")
        return None

    # Try to read the PDF and get the number of pages
    try:
        vAR_reader = PdfReader(file_path)
        vAR_num_pages = len(vAR_reader.pages)
        return file_path, vAR_num_pages
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return None

    
    
    

import os
import urllib
from PyPDF2 import PdfReader
from google.cloud import storage

def download_file(vAR_URL):
    # Decode the URL to handle any encoded characters like spaces (%20)
    vAR_URL = urllib.parse.unquote(vAR_URL)
    
    # Extract the filename from the URL
    vAR_filename = vAR_URL.split('/')[-1]
    
    # Set the directory where the file will be saved
    vAR_directory = "Result/"
    vAR_filepath = os.path.join(vAR_directory, vAR_filename)

    # Create the Result directory if it doesn't exist
    if not os.path.exists(vAR_directory):
        os.makedirs(vAR_directory)

    # Define your bucket name
    bucket_name = vAR_URL.split('/')[-2]

    # Create a storage client
    storage_client = storage.Client()

    # Get the bucket and blob
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(vAR_filename)
    
    # Download the file
    try:
        blob.download_to_filename(vAR_filepath)
        print(f"File downloaded successfully to {vAR_filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

    # Read the PDF file
    try:
        vAR_reader = PdfReader(vAR_filepath)
        vAR_num_pages = len(vAR_reader.pages)
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return None

    return vAR_filepath, vAR_num_pages
