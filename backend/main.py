from typing import List, Optional,Tuple,Any, Literal
from pydantic import Field, BaseModel
import sys, uuid, datetime 
from datetime import timedelta 
sys.path.append('./')
sys.path.append('../')

from pathlib import Path

from backend.models import *
import json
from fastapi import FastAPI 
import logging, time  
logger = logging.getLogger("xx")

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient
from azure.storage.blob import generate_container_sas, ContainerSasPermissions

app = FastAPI()

UPLOAD_FOLDER = "data"
STORAGE_ACCOUNT = "launcherstacc899"


def generate_container_sas_url( credentials, container_name, hours = 1 ):

    account_url = "https://launcherstacc899.blob.core.windows.net"
    blob_service_client = BlobServiceClient( account_url=account_url,
                                        credential=credentials)
    

    # Get user delegation key (Entra ID)
    user_delegation_key = blob_service_client.get_user_delegation_key(
            key_start_time=datetime.datetime.utcnow() - timedelta(minutes=5),
            key_expiry_time=datetime.datetime.utcnow() + timedelta(hours=hours)
        )



    sas_token = generate_container_sas(
            account_name=STORAGE_ACCOUNT,
            container_name=container_name,
            user_delegation_key=user_delegation_key,
            permission=ContainerSasPermissions(
                read=True,
                write=True,
                create=True,
                list=True
            ),
            expiry=datetime.datetime.now() + timedelta(hours=hours)
        )

    sas_url = f"{account_url}/{container_name}?{sas_token}"

    return sas_url



def start_upload_route( arg:UploadSimulatorFilesModel ):

    simulation_name = arg.simulation_name

    account_url = "https://launcherstacc899.blob.core.windows.net"
    num = uuid.uuid4()
    base_name = f"{simulation_name}XXX{num}".replace("-","").lower()   


    container_name = f"{base_name}/timestap.json"
    credentials = DefaultAzureCredential()
    service_client = BlobServiceClient( account_url=account_url,credential=credentials)
    
    try:
        
        cfg = {'creation_time':datetime.datetime.now().strftime("%d/%m/%Y") }
        container_client = service_client.get_container_client( base_name)
        container_client.create_container()    
        
        blob_client =  container_client.get_blob_client('timestamp.cfg')
        blob_client.upload_blob( json.dumps(cfg) )

        sas_token = generate_container_sas_url( credentials, container_name)

        #x = service_client.create_container(container_name)
        #logger.info('container created ' + container_name )
        #return x.container_name
        return base_name,sas_token

    except Exception as e:
        return str(e) 

    service_client.get_blob_client(container_name)

    #container_client  = storage.create_main_folder( f )
    #end_time = time.perf_counter()
    #print(f"Time taken to create container: {end_time - start_time} seconds")
    #start_time = time.perf_counter()
    #sas = storage.generate_container_sas_url( f, hours=1 )
    #end_time = time.perf_counter()
    #print(f"Time taken to generate SAS URL: {end_time - start_time} seconds")

    
    #ret = {
    #    'url': sas,
    #    'container_name': f
    #}


    #time.sleep(0.11)
    #end_upload_route( f )


    return json.dumps(ret)


@app.get('/')
async def root():
    return {'ok':'we are'}



@app.post('/start_upload')
async def start_upload(arg:UploadSimulatorFilesModel):
    print( arg.model_dump_json(indent=3))
    
    container_name,sas_token = start_upload_route( arg )
    if container_name and sas_token:
         
        print( f"{container_name} created ")
        print('totken', sas_token)
        return {'status':200, 
                'container':container_name,
                'upload_url':sas_token
                }


    return {'status',500}



@app.post('/end_upload')
async def end_upload(arg:UploadSimulatorFilesModel):

    print( arg.model_dump_json(indent=3))
    logger.info("START_UPLOAD CALLED")
    logger.info("Payload: %s", arg.model_dump())
    return {'ok':'we are --ending-- the upload'}



 

