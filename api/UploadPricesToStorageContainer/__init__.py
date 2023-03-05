import json
import requests
import os
import logging
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
    logging.info('fetching')
    response_api = requests.get('https://api.porssisahko.net/v1/latest-prices.json')
    logging.info('fetched')
    data = response_api.text
    data_obj = json.loads(data)
    container_name = "prices"

    logging.info('create clients')

    blob_service_client = BlobServiceClient.from_connection_string(
            AZURE_STORAGE_CONNECTION_STRING)

    container_client = blob_service_client.get_container_client(
            container_name)
    
    logging.info('check if exists')

    if not container_client.exists():
        logging.info('creating new container %s', container_name)
        blob_service_client.create_container(container_name)

    logging.info('crete blobss')
    for item in data_obj["prices"]:
        blob_name = f"{parse_date(item['startDate'])}.json"
        new_blob = BlobClient.from_connection_string(
            AZURE_STORAGE_CONNECTION_STRING, container_name, blob_name)
        if not new_blob.exists():
            logging.info(blob_name)
            logging.info(type(blob_name))
            logging.info('creating new blob %s', blob_name)
            new_blob.upload_blob(json.dumps(item))

    logging.info('done')
