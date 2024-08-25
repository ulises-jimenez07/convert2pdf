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
import json

from firebase_admin import db, initialize_app

import flask
from google.cloud import firestore

import vertexai
from vertexai.generative_models import GenerativeModel, Part

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
REGION = os.getenv("GCP_REGION")
MODEL_NAME="gemini-1.5-flash-001"

vertexai.init(project=PROJECT_ID, location=REGION)

#Firestore App
initialize_app()
app = flask.Flask(__name__)
db = firestore.Client(
    project=PROJECT_ID, database="testinter"
)

def get_prompt_for_summary() -> str:
    prompt = """
        You are a very professional document summarization specialist.
        Please summarize the given document.
    """
    return prompt

def insert_document_firestore(file_name: str, summary: str):
    data = {"name": file_name.split('/')[-1], "summary": summary}
    db.collection("files").document(file_name.split('/')[-1]).set(data)


def get_summary(src_bucket: str, file_name: str) -> str:

    model = GenerativeModel(MODEL_NAME)

    prompt = get_prompt_for_summary()
    if not prompt:
        return ""  
    
    pdf_file_uri = f"gs://{src_bucket}/{file_name}"
    pdf_file = Part.from_uri(pdf_file_uri, mime_type="application/pdf")
    contents = [pdf_file, prompt]

    response = model.generate_content(contents)
    return response.text

def call_convert_api(input_file): 
    output_file_name = os.path.basename(input_file)
    output_file_name = f'{output_file_name.split(".")[0]}.pdf'
    payload = {
        "input_bucket": OUTPUT_BUCKET_NAME,
        "input_file": input_file,
        "output_bucket": OUTPUT_BUCKET_NAME,
        "output_file": output_file_name,
    }
    print(payload)
    response = requests.post(PDF_CONVERTER_URL, json=payload)
    
    if response.status_code != 200:
        raise Exception(f"PDF conversion failed with status code: {response.status_code}")
    return response

def on_document_added(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
        event: event payload
        context: metadata for the event.

    TODO: 
        1. Infere mime type, if office type then
            Call call_convert_api
        2. Create CF with ENV variables for bucket reading
    """
    pubsub_message = json.loads(base64.b64decode(event["data"]).decode("utf-8"))

    if pubsub_message["contentType"] != "application/pdf":
        raise ValueError("Only PDF files are supported, aborting")

    src_bucket = pubsub_message["bucket"]
    src_fname = pubsub_message["name"]
    print(f"Processing file: gs://{src_bucket}/{src_fname}")    
   
    summary = get_summary(src_bucket, src_fname)
    print("Summary:", summary)

    insert_document_firestore(src_fname, summary)