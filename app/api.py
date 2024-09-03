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

from fastapi import FastAPI

from model import Item

from utils import upload_output
from utils import convert_file_to_pdf
from utils import download_storage_tmp

app = FastAPI()  

@app.post("/convert2pdf")
def convert2pdf(item: Item): 
    """Converts a file to PDF format and uploads the result to Cloud Storage.

    This function handles a POST request to the "/convert2pdf" endpoint. 
    It expects an `Item` object in the request body containing the input 
    bucket and file path.

    The function performs the following steps:

    1. Downloads the file from Cloud Storage.
    2. Converts the downloaded file to PDF format using LibreOffice.
    3. Uploads the converted PDF to the specified output bucket in Cloud Storage.
    4. Returns a JSON response with status code, message, and the uploaded file URL.

    Args:
        item: An Item object containing the input bucket name and file path.

    Returns:
        A dictionary containing the following keys:
            statusCode (int): HTTP status code (200 for success, 500 for error).
            message (str): Descriptive message about the conversion process.
            url (str): Public URL of the uploaded PDF file (if successful).
    """
    
    payload = {
        "statusCode": None,
        "message": None,
        "url": None
    }

    try:
        input_file_name = download_storage_tmp(item)
        output_file_name = convert_file_to_pdf(input_file_name)
        output_url = upload_output(item,output_file_name)
    except (RuntimeError, FileNotFoundError) as e:
        payload["statusCode"], payload["message"] = 500, str(e)
    except:
        payload["statusCode"], payload["message"] = 500, f"Something went wrong. Review the data provided {item}"
    else:
        payload["statusCode"] = 200
        payload["message"] = "File converted and copied successfully"
        payload["url"] = output_url
        os.remove(input_file_name)
        os.remove(output_file_name)
    finally:
        return payload