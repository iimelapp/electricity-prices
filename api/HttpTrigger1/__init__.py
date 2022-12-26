import logging
import json
import azure.functions as func
from azure.storage.blob import BlobServiceClient

AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=defaultresourcegrouab63;AccountKey=EkOzv4YeXG7s0MtFWbaCaaY2C+VoZoCLh6izbs+Q5B/Az2dafQLTv3XMhOffG3UVPKRtqq5m70Ww+AStYDKFlw==;EndpointSuffix=core.windows.net"
container_name = "prices"

def average_price(start, end, blob_service_client, container_client):
    blob_list = []

    for blob in container_client.list_blobs():
        if ((blob.name >= start) and (blob.name <= end)):
            blob_client = blob_service_client.get_blob_client(
                container_name, blob.name)
            blobr = blob_client.download_blob()
            blob_content = blobr.readall()
            datadict = json.loads(blob_content)
            blob_list.append(datadict["price"])

    average = sum(blob_list) / len(blob_list)
    return "%.2f" % float(average)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    start_time = req.params.get('START_TIME')
    end_time = req.params.get('END_TIME')

    if start_time and end_time:
        try: 
            blob_service_client = BlobServiceClient.from_connection_string(
                AZURE_STORAGE_CONNECTION_STRING)

            container_client = blob_service_client.get_container_client(
                container_name)
            average = average_price(start_time, end_time, blob_service_client, container_client)
        except Exception as exc:
            logging.error("exception", exc)
        return func.HttpResponse(f"Average price is {average}")

    else:
        return func.HttpResponse("Start time or end time missing or they are invalid", status_code=400)

