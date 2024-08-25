# Copyright 2024 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import subprocess

from model import Item

from google.cloud import storage
from google.api_core.exceptions import NotFound

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
storage_client = storage.Client(project=PROJECT_ID)

def download_storage_tmp(item: Item):
    """Downloads a file from a Google Cloud Storage bucket to a temporary file.

    Args:
        item: An Item object containing the bucket name and file path.

    Returns:
        The path of the downloaded temporary file.

    Raises:
        FileNotFoundError: If the file is not found in the bucket.
    """
    
    input_bucket = storage_client.bucket(f"gs://{item.bucket}")
    input_blob = input_bucket.blob(item.input_file_name)
    input_file_name = os.path.basename(item.input_file_name) 
    try:
        input_blob.download_to_filename(input_file_name)
    except NotFound as e:
        raise FileNotFoundError(f"File not found in bucket: {e}") from e    
    return input_file_name


def convert_file_to_pdf(input_file):
    """Converts a file to PDF format using LibreOffice.

    This function attempts to convert the provided `input_file` to a PDF 
    using LibreOffice. It assumes LibreOffice is installed and accessible 
    through the system path.

    Args:
        input_file: The path to the file to be converted.

    Raises:
        RuntimeError: If the conversion fails due to a LibreOffice error.
    """
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
    

def upload_output(item: Item, output_file_path):
    """Uploads a file to a Google Cloud Storage bucket.

    Args:
        item: An Item object containing the bucket name and file path.
        output_file_path: The path of the file to be uploaded.

    Returns:
        The public URL of the uploaded file.
    """
    output_bucket = storage_client.bucket(f"gs://{item.bucket}")
    output_blob = output_bucket.blob(item.output_file_name)
    output_blob.upload_from_filename(output_file_path)
    
    return f"gs://{item.bucket}/{item.output_file_name}"