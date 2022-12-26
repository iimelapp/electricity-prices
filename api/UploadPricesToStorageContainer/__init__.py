import json
import requests
import os
from azure.storage.blob import BlobServiceClient, BlobClient
import azure.functions as func

AZURE_STORAGE_CONNECTION_STRING = os.environ.get('AZURE_STORAGE_CONNECTION_STRING', None)

def parse_date(date):
    parsed = date.split('T')
    day = parsed[0]
    time = parsed[1]
    hour = time.split(':')[0]
    return f"{day}-{hour}"

def main(mytimer: func.TimerRequest):
    response_api = requests.get('https://api.porssisahko.net/v1/latest-prices.json')
    data = response_api.text
    data_obj = json.loads(data)
    container_name = "prices"

    blob_service_client = BlobServiceClient.from_connection_string(
            AZURE_STORAGE_CONNECTION_STRING)

    container_client = blob_service_client.get_container_client(
            container_name)

    if not container_client.exists():
        print('creating new container %s', container_name)
        blob_service_client.create_container(container_name)

    for item in data_obj["prices"]:
        blob_name = f"{parse_date(item['startDate'])}.json"
        new_blob = BlobClient.from_connection_string(
            AZURE_STORAGE_CONNECTION_STRING, container_name, blob_name)
        if not new_blob.exists():
            print('creating new blob', blob_name)
            new_blob.upload_blob(json.dumps(item))
