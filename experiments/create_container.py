
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
import datetime 
import json
import os 
from azure.storage.queue import QueueClient
from azure.storage.queue import (
    QueueClient,
    BinaryBase64EncodePolicy,
    BinaryBase64DecodePolicy
)
import base64 
import json

from azure.storage.blob import generate_container_sas, ContainerSasPermissions
from datetime import datetime, timedelta
from azure.storage.blob import generate_container_sas, ContainerSasPermissions
import time 

class Storage:

    def __init__(self, account_url):
        self.account_url = account_url
        self.credential = DefaultAzureCredential()
        #self.blob_service_client = BlobServiceClient(account_url=self.account_url, credential=self.credential)

        self.blob_service_client = BlobServiceClient(
                    account_url=self.account_url,
                    credential=self.credential
                )


    def create_folder(self, parent_folder, folder_name):
 
        blob_service_client = BlobServiceClient(account_url=self.account_url, 
        credential=self.credential)

        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S") 
        cfg = {'created_at': timestamp, 'description': 'This is a test container.'}

        container_client = blob_service_client.get_container_client( parent_folder )
        blob_client = container_client.get_blob_client(f"{folder_name}/timestamp.json")

        json_str = json.dumps(cfg)
        x = blob_client.upload_blob(json_str, overwrite=True)
        return x


    def create_main_folder(self, folder_name):
 
        blob_service_client = BlobServiceClient(account_url=self.account_url, credential=self.credential)
        x = blob_service_client.create_container(folder_name)
        return x


    def generate_container_sas_url( self, container_name, hours = 1 ):


        blob_service_client = self.blob_service_client

        # Get user delegation key (Entra ID)
        user_delegation_key = blob_service_client.get_user_delegation_key(
            key_start_time=datetime.utcnow() - timedelta(minutes=5),
            key_expiry_time=datetime.utcnow() + timedelta(hours=hours)
        )



        sas_token = generate_container_sas(
            account_name=blob_service_client.account_name,
            container_name=container_name,
            user_delegation_key=user_delegation_key,
            permission=ContainerSasPermissions(
                read=True,
                write=True,
                create=True,
                list=True
            ),
            expiry=datetime.utcnow() + timedelta(hours=hours)
        )

        sas_url = f"{self.account_url}/{container_name}?{sas_token}"

        return sas_url



import uuid

def start_upload_route( project_name = "project7" ):

    start_time = time.perf_counter()
    account_url = "https://launcherstacc899.blob.core.windows.net"
    storage = Storage(account_url)
    num = uuid.uuid4()
    f = f"{project_name}XXX{num}".replace("-","").lower()   
    container_client  = storage.create_main_folder( f )
    end_time = time.perf_counter()
    print(f"Time taken to create container: {end_time - start_time} seconds")

    start_time = time.perf_counter()
    sas = storage.generate_container_sas_url( f, hours=1 )
    end_time = time.perf_counter()
    print(f"Time taken to generate SAS URL: {end_time - start_time} seconds")

    
    ret = {
        'url': sas,
        'container_name': f
    }


    #time.sleep(0.11)
    #end_upload_route( f )


    return json.dumps(ret)


def end_upload_route( container_name ):

    print("="*100)

    # create an entry in the uploads_process queue with the container name and status "uploaded"
    account_name = os.environ["STORAGE_ACCOUNT"]
    queue_name   = os.environ["UPLOAD_QUEUE_NAME"]
    account_url = f"https://{account_name}.queue.core.windows.net"

    credential = DefaultAzureCredential()
    queue = QueueClient(
        account_url=account_url,
        queue_name=queue_name,
        credential=credential,
    )
    config = {
            'container_name':container_name,
            'status':'uploaded'
    }
    raw = json.dumps( config )
    encoded = base64.b64encode(raw.encode("utf-8")).decode("utf-8")
    x = queue.send_message( encoded )
    print(x, f"Sent message to queue {queue_name} with container name {container_name} and status 'uploaded'.")



def x(self):


    container_name = "uploads"

    # Authenticate using Entra ID (Managed Identity, CLI login, etc.)
    credential = DefaultAzureCredential()

    # Create client
    blob_service_client = BlobServiceClient(account_url=account_url, credential=credential)

    # Create container
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S") 
    cfg = {'created_at': timestamp, 'description': 'This is a test container.'}
    


    container_client = blob_service_client.get_container_client("uploads")
    blob_client = container_client.get_blob_client("project5/timestamp.json")

    json_str = json.dumps(cfg)
    blob_client.upload_blob(json_str, overwrite=True)
    #x = container_client.create_container( {'aaa': 'bbb'})
    #print(x)
    

    #try:
    #    container_client.create_container()
    #    print(f"Container '{container_name}' created.")
    #except Exception as e:
    #    print(f"Container may already exist or failed: {e}")

if __name__ == "__main__":

    # time this code to see how long it takes to create a container and send a message to the queue
    start_time = time.perf_counter()
    j = start_upload_route()
    end_time = time.perf_counter()
    print(f"Total time taken: {end_time - start_time} seconds")

    start_time = time.perf_counter()
    j = json.loads(j)
    end_upload_route( j['container_name'] )
    end_time = time.perf_counter()

    print(f"Total time taken: {end_time - start_time} seconds")


