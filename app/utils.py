import os
import subprocess

from google.cloud import storage
from google.api_core.exceptions import NotFound

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
storage_client = storage.Client(project=PROJECT_ID)

def convert_file_to_pdf(input_file):
    try:
        subprocess.run(
            f'libreoffice \
            --convert-to pdf \
            {input_file}', shell=True, check=True)
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"LibreOffice conversion failed: {e}") from e

    output_file_name = os.path.basename(input_file)
    output_file_name = f'{output_file_name.split(".")[0]}.pdf'
    if os.path.exists(output_file_name):
        return output_file_name
    else:
        return None
    
def download_storage_tmp(item: Item):
    input_bucket = storage_client.bucket(item.input_bucket)
    input_blob = input_bucket.blob(item.input_file)
    input_file_name = os.path.basename(item.input_file) 
    try:
        input_blob.download_to_filename(input_file_name)
    except NotFound as e:
        raise FileNotFoundError(f"File not found in bucket: {e}") from e    
    return input_file_name

def upload_output(item: Item,output_file_path):
    output_bucket = storage_client.bucket(item.output_bucket)
    output_blob = output_bucket.blob(item.output_file)
    output_blob.upload_from_filename(output_file_path)
    return f"gs://{item.output_bucket}/{item.output_file}"