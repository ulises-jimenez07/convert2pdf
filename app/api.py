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

from utils import download_storage_tmp
from utils import convert_file_to_pdf
from utils import upload_output

app = FastAPI()  

@app.post("/convert2pdf")
def convert2pdf(item: Item): 
    
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
        payload["statusCode"], payload["message"] = 500, e

    else:
        payload["statusCode"] = 200
        payload["message"] = "File converted and copied successfully"
        payload["url"] = output_url
    
    finally:
        os.remove(input_file_name)
        os.remove(output_file_name)

        return payload
