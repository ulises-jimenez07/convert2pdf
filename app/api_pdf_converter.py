#  Copyright 2024 Google. This software is provided as-is, without warranty or
#  representation for any use or purpose.
#  Your use of it is subject to your agreement with Google

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from google.cloud import storage
from google.api_core.exceptions import NotFound

import os
import subprocess

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
storage_client = storage.Client(project=PROJECT_ID)

class Item(BaseModel):
    input_bucket: str
    input_file: str 
    output_bucket: str
    output_file: str | None = None


app = FastAPI()

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
    return output_blob.self_link
    
@app.post("/convert2pdf")
async def create_item(item: Item): 
    try:
        input_file_name = download_storage_tmp(item)
        output_file_name = convert_file_to_pdf(input_file_name)
        output_url = upload_output(item,output_file_name)
        
        os.remove(input_file_name)
        os.remove(output_file_name)
        
        return {"message": "File converted and copied successfully", "url": output_url}
    except (RuntimeError, FileNotFoundError) as e:
        raise HTTPException(status_code=500, detail=str(e)) from e